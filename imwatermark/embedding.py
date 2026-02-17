
import cv2
import numpy as np
import pywt

def watermark_embedding(cover_path, watermark_path, alpha, beta):
    """
    Embeds a watermark into a cover image using DWT-DCT-QIM.
    
    Args:
        cover_path (str): Path to the cover image.
        watermark_path (str): Path to the watermark image.
        alpha (float): Step size parameter.
        beta (float): Normalization constant for variance.
        
    Returns:
        tuple: (watermarked_img (np.array), watermark_resized (np.array))
    """
    # 1. Read Images
    cover = cv2.imread(cover_path)
    if cover is None:
        raise FileNotFoundError(f"Cover image not found: {cover_path}")
    
    # Convert BGR to RGB (OpenCV uses BGR by default)
    cover = cv2.cvtColor(cover, cv2.COLOR_BGR2RGB)
    
    watermark = cv2.imread(watermark_path)
    if watermark is None:
        raise FileNotFoundError(f"Watermark image not found: {watermark_path}")

    # Ensure cover is RGB
    if len(cover.shape) != 3 or cover.shape[2] != 3:
        raise ValueError('Cover image must be RGB for YCbCr conversion.')

    # Resize cover to be multiple of 8
    rows, cols, _ = cover.shape
    new_rows = (rows // 8) * 8
    new_cols = (cols // 8) * 8
    if new_rows != rows or new_cols != cols:
        cover = cv2.resize(cover, (new_cols, new_rows))

    # 2. Convert to YCbCr and Get Y Channel
    cover_ycbcr = cv2.cvtColor(cover, cv2.COLOR_RGB2YCrCb)
    
    Y = cover_ycbcr[:, :, 0].astype(np.float32)
    
    # 3. Apply DWT (Level 1 Haar)
    coeffs = pywt.dwt2(Y, 'haar')
    LL, (LH, HL, HH) = coeffs
    
    # Determine capacity
    sub_rows, sub_cols = LL.shape
    block_size = 4
    
    wm_rows = sub_rows // block_size
    wm_cols = sub_cols // block_size
    
    # Prepare Watermark
    if len(watermark.shape) == 3:
        watermark_gray = cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY)
    else:
        watermark_gray = watermark

    # Binarize
    _, watermark_bin = cv2.threshold(watermark_gray, 128, 1, cv2.THRESH_BINARY)
    
    # Resize watermark to fit the capacity
    watermark_resized = cv2.resize(watermark_bin, (wm_cols, wm_rows), interpolation=cv2.INTER_NEAREST)
    
    # 4-6. Embed in all subbands
    subbands = [LL, LH, HL, HH]
    embedded_subbands = []
    
    for k in range(4):
        sb = subbands[k].copy()
        
        # Iterate over 4x4 blocks
        for r in range(wm_rows):
            for c in range(wm_cols):
                # Block indices
                r_start = r * block_size
                r_end = r_start + block_size
                c_start = c * block_size
                c_end = c_start + block_size
                
                block = sb[r_start:r_end, c_start:c_end]
                
                # 5. DCT on block
                dct_block = cv2.dct(block)
                dct_block_orig = dct_block.copy()
                
                # Adaptive step size
                dct_vec = dct_block.flatten()
                dct_remaining = dct_vec[1:] # Exclude DC (index 0)
                
                # Use ddof=1 to match MATLAB's var() (sample variance)
                block_var = np.var(dct_remaining, ddof=1) if len(dct_remaining) > 0 else 0
                
                s = alpha * (1 + block_var / beta)
                
                if s < 1e-6:
                    s = 1e-6
                
                # Robustness check for s
                if s < 10:
                    s = 10.0
                
                # QIM Embedding on DC coefficient (0,0)
                coeff_idx = (0, 0)
                coeff = dct_block[coeff_idx]
                
                wb = watermark_resized[r, c]
                
                # Quantization
                q = round(coeff / s)
                
                # Embed bit
                if wb == 0:
                    # Make even
                    q_prime = 2 * np.floor(q / 2)
                else:
                    # Make odd
                    q_prime = 2 * np.floor(q / 2) + 1
                    
                # Reconstruction
                dct_block[coeff_idx] = q_prime * s
                
                # IDCT
                new_block = cv2.idct(dct_block)
                sb[r_start:r_end, c_start:c_end] = new_block
                
                # Debug print similar to MATLAB
                if k == 0 and r == 0 and c == 0:
                    print('\n--- DEBUG: Embedding First Block (LL Subband) ---')
                    print('Original 4x4 Block:\n', block)
                    print('DCT of Block:\n', dct_block_orig)
                    print(f'Variance (AC only): {block_var:.4f}')
                    print(f'Alpha: {alpha:.2f}, Beta: {beta:.2f}')
                    print(f'Adaptive Step (s): {s:.4f}')
                    print(f'DCT(0,0) Coefficient: {coeff:.4f}')
                    print(f'Watermark Bit to Embed: {wb}')
                    print(f'Quantized (q): {q}')
                    print(f'Modified Quantized (q_prime): {q_prime}')
                    print('Modified DCT Block:\n', dct_block)
                    print('IDCT (Watermarked Block):\n', new_block)
                    print('---------------------------------------------')
                    
        embedded_subbands.append(sb)
        
    # 8. Reconstruct Image
    new_coeffs = (embedded_subbands[0], (embedded_subbands[1], embedded_subbands[2], embedded_subbands[3]))
    Y_watermarked = pywt.idwt2(new_coeffs, 'haar')
    
    # Handle dimension mismatch if any (due to DWT boundary effects sometimes)
    Y_watermarked = Y_watermarked[:Y.shape[0], :Y.shape[1]]

    # Clip values
    np.clip(Y_watermarked, 0, 255, out=Y_watermarked)
    
    # Reconstruct YCbCr
    watermarked_ycbcr = cover_ycbcr.copy()
    watermarked_ycbcr[:, :, 0] = Y_watermarked.astype(np.uint8)
    
    # Convert back to RGB
    watermarked_img = cv2.cvtColor(watermarked_ycbcr, cv2.COLOR_YCrCb2RGB)
    
    return watermarked_img, watermark_resized
