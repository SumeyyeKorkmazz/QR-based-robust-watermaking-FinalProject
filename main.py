
import cv2
import os
import sys
import numpy as np

# Ensure output encoding is UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Import metadata config
from watermark_config import WATERMARK_METADATA

# Import from the modular package
from imwatermark.embedding import watermark_embedding
from imwatermark.extraction import watermark_extraction
from imwatermark.metrics import calculate_psnr, calculate_ssim, calculate_nc, calculate_ber
from imwatermark.visualization import visualize_results
from imwatermark.watermark_generation import WatermarkGenerator
from imwatermark.qr_utils import decode_qr_code

def main():
    # ----------------------------------------------------------------
    # Settings
    # ----------------------------------------------------------------
    cover_path = 'cover_image.png'
    alpha = 0.5
    beta  = 100.0

    if not os.path.exists(cover_path):
        print(f"Error: {cover_path} not found.")
        sys.exit(1)

    print('--- Digital Image Watermarking Process Started ---')
    print(f'Parameters: Alpha = {alpha:.2f}, Beta = {beta:.2f}')

    # ----------------------------------------------------------------
    # Step 0: Generate QR watermark from config metadata
    # ----------------------------------------------------------------
    print('\n[Step 0] Generating QR-code watermark from metadata...')
    print(f'  Producer  : {WATERMARK_METADATA["producer"]}')
    print(f'  Date      : {WATERMARK_METADATA["date"]}')
    print(f'  AI Model  : {WATERMARK_METADATA["ai_model"]}')

    generator = WatermarkGenerator(version=10, error_correction='H')
    qr_watermark = generator.generate_watermark(WATERMARK_METADATA)   # 64×64 binary (0/1)

    # Save QR watermark as a PNG so watermark_embedding() can read it by path
    qr_watermark_path = 'watermark_qr.png'
    cv2.imwrite(qr_watermark_path, (qr_watermark * 255).astype(np.uint8))
    print(f'  QR watermark saved to: {qr_watermark_path}  (shape: {qr_watermark.shape})')

    # ----------------------------------------------------------------
    # Step 1: Embedding
    # ----------------------------------------------------------------
    print('\n[Step 1] Initializing Embedding Process...')
    watermarked_img, original_watermark_resized = watermark_embedding(
        cover_path, qr_watermark_path, alpha, beta
    )

    # Save the watermarked image
    output_filename = 'watermarked_image_py.png'
    cv2.imwrite(output_filename, cv2.cvtColor(watermarked_img, cv2.COLOR_RGB2BGR))
    print(f'Watermarked image saved to: {output_filename}')

    # ----------------------------------------------------------------
    # Step 2: Quality metrics (cover vs watermarked)
    # ----------------------------------------------------------------
    cover_img = cv2.imread(cover_path)
    cover_img = cv2.cvtColor(cover_img, cv2.COLOR_BGR2RGB)

    h, w, _ = watermarked_img.shape
    cover_resized = cv2.resize(cover_img, (w, h))

    psnr_val = calculate_psnr(cover_resized, watermarked_img)
    ssim_val = calculate_ssim(cover_resized, watermarked_img)

    print('\n[Step 2] Quality Metrics (Cover vs Watermarked):')
    print(f'   PSNR: {psnr_val:.2f} dB')
    print(f'   SSIM: {ssim_val:.4f}')

    # ----------------------------------------------------------------
    # Step 3: Extraction
    # ----------------------------------------------------------------
    print('\n[Step 3] Initializing Extraction Process...')
    wm_rows, wm_cols = original_watermark_resized.shape
    extracted_watermark = watermark_extraction(watermarked_img, wm_rows, wm_cols, alpha, beta)

    # ----------------------------------------------------------------
    # Step 4: Extraction accuracy metrics
    # ----------------------------------------------------------------
    nc_val  = calculate_nc(original_watermark_resized, extracted_watermark)
    ber_val = calculate_ber(original_watermark_resized, extracted_watermark)

    print('\n[Step 4] Extraction Metrics (Original vs Extracted Watermark):')
    print(f'   Normalized Correlation (NC): {nc_val:.4f}')
    print(f'   Bit Error Rate (BER):        {ber_val:.4f}')

    # ----------------------------------------------------------------
    # Step 5: Decode QR from extracted watermark
    # ----------------------------------------------------------------
    print('\n[Step 5] Decoding QR code from extracted watermark...')
    decoded_metadata = decode_qr_code(extracted_watermark)
    if decoded_metadata:
        print(f'   ✅ Decoded metadata: {decoded_metadata}')
    else:
        print('   ⚠️  Could not decode QR code from extracted watermark.')
        print('      (This can happen due to embedding distortion — NC/BER above shows accuracy)')

    # ----------------------------------------------------------------
    # Step 6: Visualization
    # ----------------------------------------------------------------
    visualize_results(cover_resized, watermarked_img, original_watermark_resized, extracted_watermark, psnr_val, nc_val)

    print('\n--- Process Completed Successfully ---')

if __name__ == "__main__":
    main()
