
# Digital Image Watermarking (DWT-DCT-QIM)

This project implements a robust digital image watermarking algorithm using **Discrete Wavelet Transform (DWT)**, **Discrete Cosine Transform (DCT)**, and **Quantization Index Modulation (QIM)**. It is a Python implementation originally translated and refactored from MATLAB.

## Features

- **Hybrid Domain embedding**: Combines DWT and DCT for better robustness and imperceptibility.
- **QIM (Quantization Index Modulation)**: Used for embedding watermark bits into the DC coefficients of DCT blocks.
- **Adaptive Step Size**: The quantization step size is adapted based on the variance of the block, enhancing visual quality.
- **Modular Design**: The codebase is organized into a Python package structure (`imwatermark`) for better maintainability and extensibility.
- **Comprehensive Metrics**: Calculates and displays:
  - **PSNR** (Peak Signal-to-Noise Ratio)
  - **SSIM** (Structural Similarity Index)
  - **NC** (Normalized Correlation)
  - **BER** (Bit Error Rate)

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

## Installation

1. Clone the repository or extract the project files.
2. Navigate to the project directory:
   ```bash
   cd image_watermarking
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your cover image (e.g., `cover_image.png`) and watermark image (e.g., `watermark.png`) in the project root directory.
2. Run the main script:
   ```bash
   python main.py
   ```

The script will perform the following steps:
1.  **Embedding**: Embeds `watermark.png` into `cover_image.png`.
2.  **Quality Evaluation**: Calculates PSNR and SSIM between the original and watermarked images.
3.  **Saving**: Saves the result as `watermarked_image_py.png`.
4.  **Extraction**: Extracts the watermark from the watermarked image.
5.  **Accuracy Evaluation**: Calculates NC and BER between the original and extracted watermarks.
6.  **Visualization**: Displays the original cover, watermarked image, original watermark, and extracted watermark side-by-side.

## Project Structure

```
image_watermarking/
├── imwatermark/             # Core package
│   ├── __init__.py
│   ├── embedding.py         # Watermark embedding logic
│   ├── extraction.py        # Watermark extraction logic
│   ├── metrics.py           # PSNR, SSIM, NC, BER calculations
│   └── visualization.py     # Plotting results
├── main.py                  # Entry point script
├── requirements.txt         # Project dependencies
├── CHANGELOG.md             # Version history
└── README.md                # Project documentation
```

## Algorithm Details

1.  **Preprocessing**: The cover image is converted to YCbCr color space, and only the Y (Luminance) channel is used.
2.  **DWT**: 1-level Haar DWT is applied to the Y channel to obtain LL, LH, HL, HH subbands.
3.  **Blocking**: Each subband is divided into 4x4 non-overlapping blocks.
4.  **DCT**: DCT is applied to each block.
5.  **Embedding**: The watermark bit is embedded into the DC coefficient (0,0) of the DCT block using QIM with an adaptive step size.
6.  **Inverse Transforms**: IDCT and Inverse DWT are applied to reconstruct the watermarked image.
7.  **Extraction**: The reverse process is applied. The watermark bit is extracted by checking the quantization level of the DC coefficient. Majority voting across the 4 subbands improves robustness.

## Version

Current Version: **1.0.0** (See `CHANGELOG.md` for details)
