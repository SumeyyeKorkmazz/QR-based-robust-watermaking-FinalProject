
import matplotlib.pyplot as plt

def visualize_results(cover_img, watermarked_img, original_watermark, extracted_watermark, psnr_val, nc_val):
    """
    Visualize the watermarking results using Matplotlib.
    
    Args:
        cover_img: Original cover image.
        watermarked_img: Watermarked image.
        original_watermark: Original watermark image (binary).
        extracted_watermark: Extracted watermark image (binary).
        psnr_val: PSNR value to display in title.
        nc_val: NC value to display in title.
    """
    plt.figure('Watermarking Results', figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(cover_img)
    plt.title('Original Cover Image')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(watermarked_img)
    plt.title(f'Watermarked Image (PSNR: {psnr_val:.2f} dB)')
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(original_watermark, cmap='gray')
    plt.title('Original Watermark (Binary)')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(extracted_watermark, cmap='gray')
    plt.title(f'Extracted Watermark (NC: {nc_val:.4f})')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
