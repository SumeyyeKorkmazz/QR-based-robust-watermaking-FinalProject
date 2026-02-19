import numpy as np
import qrcode
import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image
from typing import Optional

def generate_qr_code_image(
    metadata: str,
    version: int = 10,
    error_correction: str = 'H',
    target_size: tuple[int, int] = (64, 64),
) -> np.ndarray:
    """Versiyon 10 QR üretir ve 64x64 merkeze sabitler."""
    ecc_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=version,
        error_correction=ecc_levels[error_correction],
        box_size=1,
        border=0,
    )
    qr.add_data(metadata)
    qr.make(fit=False)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("L")
    qr_array = np.array(qr_img) # 57x57

    # 64x64 Beyaz zemine yerleştir
    final_qr = np.ones(target_size, dtype=np.uint8) * 255
    y_off = (target_size[0] - qr_array.shape[0]) // 2
    x_off = (target_size[1] - qr_array.shape[1]) // 2
    final_qr[y_off:y_off+qr_array.shape[0], x_off:x_off+qr_array.shape[1]] = qr_array

    return (final_qr < 127).astype(np.uint8)

def decode_qr_code(qr_array: np.ndarray) -> Optional[str]:
    """Zırhlı Decode: Görüntüyü temizler, büyütür ve çerçeve ekler."""
    if qr_array is None:
        return None

    # 1. 0-255 uint8 formatına çevir
    img = (qr_array * 255).astype(np.uint8)
    
    # 2. Boyutu devasa yap (512x512) - Keskinliği korumak için NEAREST
    img_resized = cv2.resize(img, (512, 512), interpolation=cv2.INTER_NEAREST)
    
    # 3. GENİŞ Beyaz Çerçeve Ekle (Quiet Zone simülasyonu)
    # Telefonun okumasını sağlayan kritik boşluk
    img_padded = cv2.copyMakeBorder(
        img_resized, 100, 100, 100, 100, 
        cv2.BORDER_CONSTANT, value=[255, 255, 255]
    )

    # 4. Binary Threshold (Gri pikselleri yok et)
    _, img_binary = cv2.threshold(img_padded, 128, 255, cv2.THRESH_BINARY)

    # 5. Farklı varyasyonları dene
    def try_decode(image):
        decoded = pyzbar_decode(image)
        if decoded:
            return decoded[0].data.decode('utf-8')
        return None

    # Normal deneme
    res = try_decode(img_binary)
    if res: return res

    # Hafif yumuşatılmış deneme (Bazı kütüphaneler keskin pikselleri sevmez)
    img_blur = cv2.GaussianBlur(img_binary, (3,3), 0)
    res = try_decode(img_blur)
    if res: return res

    # Görüntüyü ters çevirip deneme
    img_inv = cv2.bitwise_not(img_binary)
    res = try_decode(img_inv)
    
    return res