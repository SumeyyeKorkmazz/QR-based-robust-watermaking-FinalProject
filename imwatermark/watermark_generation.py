"""
Damga Üretme Modülü (Watermark Generation Module)
Bu modül, kullanıcı bilgilerini QR kod formatında damga olarak üretir.
"""

from typing import Dict

import numpy as np

from .qr_utils import generate_qr_code_image


class WatermarkGenerator:
    """
    QR kod tabanlı damga üretici sınıfı.
    Kullanıcı bilgilerini, üretim tarihini ve YZ modelini içeren
    metaveri dizisini 64x64 boyutunda QR koda dönüştürür.
    """
    
    def __init__(self, version: int = 10, error_correction: str = 'H'):
        """
        WatermarkGenerator sınıfını başlatır.
        
        Args:
            version: QR kod versiyonu (varsayılan: 10, 57x57 modül)
            error_correction: Hata düzeltme seviyesi ('L', 'M', 'Q', 'H')
                             varsayılan: 'H' (%30 hata toleransı)
        """
        self.version = version
        self.error_correction = error_correction
        self.target_size = (64, 64)
        
        self.ecc_levels = None  # qr_utils içinde yönetiliyor

    def create_metadata_string(self, user_info: Dict[str, str]) -> str:
        """
        Kullanıcı bilgilerinden metaveri dizisi oluşturur.
        
        Args:
            user_info: Kullanıcı bilgilerini içeren dictionary
                     - 'producer': Üretici adı-soyadı (≈50 karakter)
                     - 'date': Üretim tarihi (≈10 karakter)
                     - 'ai_model': Kullanılan YZ modeli (≈50 karakter)
        
        Returns:
            Metaveri dizisi (string)
        """
        producer = user_info.get('producer', '')
        date = user_info.get('date', '')
        ai_model = user_info.get('ai_model', '')
        
        # Metaveri formatı: producer|date|ai_model
        metadata = f"{producer}|{date}|{ai_model}"
        
        return metadata
    
    def generate_qr_code(self, metadata: str) -> np.ndarray:
        """
        Metaveri dizisinden QR kod oluşturur.
        
        Args:
            metadata: Gömülecek metaveri dizisi
        
        Returns:
            64x64 boyutunda binary (0-1) numpy array
        """
        qr_array_binary = generate_qr_code_image(
            metadata=metadata,
            version=self.version,
            error_correction=self.error_correction,
            target_size=self.target_size,
        )
        return qr_array_binary
    
    def generate_watermark(self, user_info: Dict[str, str]) -> np.ndarray:
        """
        Kullanıcı bilgilerinden damga (watermark) üretir.
        
        Args:
            user_info: Kullanıcı bilgilerini içeren dictionary
        
        Returns:
            64x64 boyutunda binary watermark array
        """
        # Metaveri dizisi oluştur
        metadata = self.create_metadata_string(user_info)
        
        # QR kod oluştur
        watermark = self.generate_qr_code(metadata)
        
        return watermark
    
    @staticmethod
    def watermark_to_bit_sequence(watermark: np.ndarray) -> np.ndarray:
        """
        Watermark matrisini bit dizisine dönüştürür.
        
        Args:
            watermark: 64x64 boyutunda binary watermark array
        
        Returns:
            4096 bitlik (64x64) bit dizisi
        """
        # Satır-sütun sırasına göre düzleştir
        bit_sequence = watermark.flatten()
        
        return bit_sequence

