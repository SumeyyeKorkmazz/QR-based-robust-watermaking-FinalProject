
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-17

### Added
- Initial release of the Python implementation of the DWT-DCT-QIM Image Watermarking project.
- Modular `imwatermark` package structure containing:
  - `embedding.py`: Watermark embedding logic.
  - `extraction.py`: Watermark extraction logic.
  - `metrics.py`: Utility functions for PSNR, SSIM, NC, and BER calculations.
  - `visualization.py`: Helper functions for visualizing results using Matplotlib.
- `main.py`: Entry point for running the watermarking process.
- `requirements.txt`: List of project dependencies.
