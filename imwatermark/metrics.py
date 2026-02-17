
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(image_true, image_test):
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR).
    """
    return psnr(image_true, image_test)

def calculate_ssim(image_true, image_test):
    """
    Calculate Structural Similarity Index (SSIM).
    Assumes RGB images (channel_axis=2).
    """
    return ssim(image_true, image_test, channel_axis=2)

def calculate_nc(original_watermark, extracted_watermark):
    """
    Calculate Normalized Correlation (NC) between original and extracted watermarks.
    """
    original_flat = original_watermark.flatten().astype(float)
    extracted_flat = extracted_watermark.flatten().astype(float)

    if np.sum(original_flat) == 0 and np.sum(extracted_flat) == 0:
        return 1.0
    
    numerator = np.sum(original_flat * extracted_flat)
    denominator = np.sqrt(np.sum(original_flat**2)) * np.sqrt(np.sum(extracted_flat**2))
    
    if denominator == 0:
        return 0.0 # Standard handling (though unlikely if both are 0 handled above)
        
    return numerator / denominator

def calculate_ber(original_watermark, extracted_watermark):
    """
    Calculate Bit Error Rate (BER) between original and extracted watermarks.
    """
    original_flat = original_watermark.flatten().astype(float)
    extracted_flat = extracted_watermark.flatten().astype(float)
    
    diff = np.abs(original_flat - extracted_flat)
    if len(diff) == 0:
        return 0.0
        
    return np.sum(diff) / len(diff)
