import os
import sys
import numpy as np
import cv2
from datetime import datetime

# Imwatermark ana dizinini scripte dahil edelim (OOP wrapper için)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from imwatermark.embedding import watermark_embedding
from imwatermark.extraction import watermark_extraction
from imwatermark.watermark_generation import WatermarkGenerator
from imwatermark.qr_utils import decode_qr_code

class WatermarkService:
    def __init__(self, alpha: float = 0.5, beta: float = 100.0):
        self.alpha = alpha
        self.beta = beta
        self.generator = WatermarkGenerator(version=10, error_correction='H')

    def generate_qr_watermark(self, user_name: str, date_str: str, ai_model: str, output_path: str) -> np.ndarray:
        """
        Metadata alip QR kodu uretir ve kaydeder.
        """
        metadata = {
            "producer": user_name,
            "date": date_str,
            "ai_model": ai_model
        }
        qr_watermark = self.generator.generate_watermark(metadata)
        cv2.imwrite(output_path, (qr_watermark * 255).astype(np.uint8))
        return qr_watermark

    def embed_watermark(self, cover_path: str, qr_watermark_path: str, output_watermarked_path: str):
        """
        Gorsele QR kod damgasini gomer. DWT-DCT kodu cagrilir.
        """
        watermarked_img, _ = watermark_embedding(
            cover_path, qr_watermark_path, self.alpha, self.beta
        )
        # BGR'a cevirip kaydet (OpenCV save format)
        cv2.imwrite(output_watermarked_path, cv2.cvtColor(watermarked_img, cv2.COLOR_RGB2BGR))
        return output_watermarked_path

    def extract_and_decode(self, watermarked_img_path: str):
        """
        Damgayi gorselden cikartir ve QR icerigini okur.
        wm_rows ve wm_cols embedding ile aynı formülle hesaplanır.
        """
        # Goruntuyu RGB olarak oku
        img = cv2.imread(watermarked_img_path)
        if img is None:
            raise ValueError("Görüntü bulunamadı veya okunamadı.")

        watermarked_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Embedding ile aynı mantıkla wm_rows/wm_cols hesapla:
        # 1. Görüntüyü 8'e bölen boyuta kırp (embedding de yapıyor)
        rows, cols, _ = watermarked_img.shape
        new_rows = (rows // 8) * 8
        new_cols = (cols // 8) * 8
        if new_rows != rows or new_cols != cols:
            watermarked_img = cv2.resize(watermarked_img, (new_cols, new_rows))

        # 2. YCbCr → Y
        import pywt
        img_ycbcr = cv2.cvtColor(watermarked_img, cv2.COLOR_RGB2YCrCb)
        Y = img_ycbcr[:, :, 0].astype(np.float32)

        # 3. DWT boyutu
        coeffs = pywt.dwt2(Y, 'haar')
        LL, _ = coeffs
        sub_rows, sub_cols = LL.shape

        # 4. Embedding ile aynı formül
        block_size = 4
        wm_rows = sub_rows // block_size
        wm_cols = sub_cols // block_size

        print(f"[Extract] Image: {new_rows}x{new_cols} → LL: {sub_rows}x{sub_cols} → WM: {wm_rows}x{wm_cols}")

        extracted_watermark = watermark_extraction(
            watermarked_img, wm_rows, wm_cols, self.alpha, self.beta
        )
        decoded_metadata = decode_qr_code(extracted_watermark)
        return decoded_metadata

