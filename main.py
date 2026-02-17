
import cv2
import os
import sys

# Ensure output encoding is UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Import from the modular package
from imwatermark.embedding import watermark_embedding
from imwatermark.extraction import watermark_extraction
from imwatermark.metrics import calculate_psnr, calculate_ssim, calculate_nc, calculate_ber
from imwatermark.visualization import visualize_results

def main():
    # Settings
    cover_path = 'cover_image.png'
    watermark_path = 'watermark.png'

    if not os.path.exists(cover_path):
        print(f"Error: {cover_path} not found.")
        sys.exit(1)
    if not os.path.exists(watermark_path):
        print(f"Error: {watermark_path} not found.")
        sys.exit(1)

    alpha = 0.5
    beta = 100.0

    print('--- Digital Image Watermarking Process Started ---')
    print(f'Parameters: Alpha = {alpha:.2f}, Beta = {beta:.2f}')

    # --- 1. Embedding ---
    print('\n[Step 1] Initializing Embedding Process...')
    watermarked_img, original_watermark_resized = watermark_embedding(cover_path, watermark_path, alpha, beta)

    # Save the watermarked image
    output_filename = 'watermarked_image_py.png'
    # OpenCV saves as BGR
    cv2.imwrite(output_filename, cv2.cvtColor(watermarked_img, cv2.COLOR_RGB2BGR))
    print(f'Watermarked image saved to: {output_filename}')

    # --- 2. Evaluate Quality of Watermarked Image ---
    cover_img = cv2.imread(cover_path)
    # Convert BGR to RGB
    cover_img = cv2.cvtColor(cover_img, cv2.COLOR_BGR2RGB)

    # Resize cover to match watermarked image for fair PSNR calculation
    h, w, _ = watermarked_img.shape
    cover_resized = cv2.resize(cover_img, (w, h))

    # Calculate Metrics
    psnr_val = calculate_psnr(cover_resized, watermarked_img)
    ssim_val = calculate_ssim(cover_resized, watermarked_img)

    print('\n[Step 2] Quality Metrics (Cover vs Watermarked):')
    print(f'   PSNR: {psnr_val:.2f} dB')
    print(f'   SSIM: {ssim_val:.4f}')

    # --- 3. Extraction ---
    print('\n[Step 3] Initializing Extraction Process...')
    wm_rows, wm_cols = original_watermark_resized.shape
    extracted_watermark = watermark_extraction(watermarked_img, wm_rows, wm_cols, alpha, beta)

    # --- 4. Evaluate Extraction Accuracy ---
    nc_val = calculate_nc(original_watermark_resized, extracted_watermark)
    ber_val = calculate_ber(original_watermark_resized, extracted_watermark)

    print('\n[Step 4] Extraction Metrics (Original Watermark vs Extracted):')
    print(f'   Normalized Correlation (NC): {nc_val:.4f}')
    print(f'   Bit Error Rate (BER): {ber_val:.4f}')

    # --- 5. Visualization ---
    visualize_results(cover_resized, watermarked_img, original_watermark_resized, extracted_watermark, psnr_val, nc_val)

    print('\n--- Process Completed Successfully ---')

if __name__ == "__main__":
    main()
