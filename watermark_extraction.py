
import numpy as np
import cv2
import pywt
from scipy import stats

def watermark_extraction(watermarked_img, wm_rows, wm_cols, alpha, beta):
    # Convert to YCbCr and get Y
    # OpenCV YCrCb: Y=0
    img_ycbcr = cv2.cvtColor(watermarked_img, cv2.COLOR_RGB2YCrCb)
    Y = img_ycbcr[:, :, 0].astype(np.float32)
    
    # DWT Level 1
    coeffs = pywt.dwt2(Y, 'haar')
    LL, (LH, HL, HH) = coeffs
    subbands = [LL, LH, HL, HH]
    
    block_size = 4
    
    # Storage for extracted bits
    # Shape: (wm_rows, wm_cols, 4)
    extracted_bits = np.zeros((wm_rows, wm_cols, 4), dtype=int)
    
    for k in range(4):
        sb = subbands[k]
        
        for r in range(wm_rows):
            for c in range(wm_cols):
                r_start = r * block_size
                c_start = c * block_size
                
                # Boundary check
                if r_start + block_size > sb.shape[0] or c_start + block_size > sb.shape[1]:
                    continue
                    
                block = sb[r_start:r_start+block_size, c_start:c_start+block_size]
                
                # DCT
                dct_block = cv2.dct(block)
                
                # Variance (using watermarked block)
                dct_vec = dct_block.flatten()
                dct_remaining = dct_vec[1:] # Exclude DC (1,1) (Carrying Watermark)
                block_var = np.var(dct_remaining, ddof=1) if len(dct_remaining) > 0 else 0
                
                # Adaptive step calculation
                s = alpha * (1 + block_var / beta)
                if s < 10:
                    s = 10.0
                
                # Extraction Logic
                coeff = dct_block[0, 0]
                q = round(coeff / s)
                
                # Parity check
                if q % 2 == 0:
                    extracted_bits[r, c, k] = 0
                else:
                    extracted_bits[r, c, k] = 1
                
                # DEBUG for first block
                if k == 0 and r == 0 and c == 0:
                    print('\n--- DEBUG: Extraction First Block (LL Subband) ---')
                    print('Watermarked 4x4 Block:\n', block)
                    print('DCT of Block:\n', dct_block)
                    print(f'Variance (AC only): {block_var:.4f}')
                    print(f'Alpha: {alpha:.2f}, Beta: {beta:.2f}')
                    print(f'Adaptive Step (s): {s:.4f}')
                    print(f'DCT(0,0) Coefficient: {coeff:.4f}')
                    print(f'Quantized (q): {q}')
                    print(f'Extracted Bit: {extracted_bits[r, c, k]}')
                    print('---------------------------------------------')

    # Majority Voting
    # "çoğunluk alt banttan elde edilen damga biti doğru olarak kabul edilerek"
    # Using mode
    mode_res = stats.mode(extracted_bits, axis=2, keepdims=True)
    extracted_watermark = mode_res.mode.squeeze(axis=2)
    # The squeeze might remove wm_cols if it was 1, so be careful.
    # However, wm_cols is usually > 1. 
    # If wm_rows or wm_cols is 1, squeeze might be aggressive if not specifying axis properly? 
    # squeeze(axis=2) is safe.
    
    return extracted_watermark
