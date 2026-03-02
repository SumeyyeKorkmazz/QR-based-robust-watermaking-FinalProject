"""
Watermark Generation Module
This module generates user information as a watermark in QR code format.
"""

from typing import Dict

import numpy as np

from .qr_utils import generate_qr_code_image


class WatermarkGenerator:
    """
    QR code-based watermark generator class.
    Converts the metadata string containing user information, production date,
    and AI model into a 64x64 QR code.
    """
    
    def __init__(self, version: int = 10, error_correction: str = 'H'):
        """
        Initializes the WatermarkGenerator class.
        
        Args:
            version: QR code version (default: 10, 57x57 modules)
            error_correction: Error correction level ('L', 'M', 'Q', 'H')
                             default: 'H' (30% error tolerance)
        """
        self.version = version
        self.error_correction = error_correction
        self.target_size = (64, 64)
        
        self.ecc_levels = None  # Managed inside qr_utils

    def create_metadata_string(self, user_info: Dict[str, str]) -> str:
        """
        Creates a metadata string from user information.
        
        Args:
            user_info: Dictionary containing user information
                     - 'producer': Producer full name (~50 characters)
                     - 'date': Production date (~10 characters)
                     - 'ai_model': AI model used (~50 characters)
        
        Returns:
            Metadata string
        """
        producer = user_info.get('producer', '')
        date = user_info.get('date', '')
        ai_model = user_info.get('ai_model', '')
        
        # Metadata format: producer|date|ai_model
        metadata = f"{producer}|{date}|{ai_model}"
        
        return metadata
    
    def generate_qr_code(self, metadata: str) -> np.ndarray:
        """
        Generates a QR code from the metadata string.
        
        Args:
            metadata: Metadata string to be embedded
        
        Returns:
            64x64 binary (0-1) numpy array
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
        Generates a watermark from user information.
        
        Args:
            user_info: Dictionary containing user information
        
        Returns:
            64x64 binary watermark array
        """
        # Create metadata string
        metadata = self.create_metadata_string(user_info)
        
        # Generate QR code
        watermark = self.generate_qr_code(metadata)
        
        return watermark
    
    @staticmethod
    def watermark_to_bit_sequence(watermark: np.ndarray) -> np.ndarray:
        """
        Converts the watermark matrix into a bit sequence.
        
        Args:
            watermark: 64x64 binary watermark array
        
        Returns:
            4096-bit (64x64) bit sequence
        """
        # Flatten in row-major (C) order
        bit_sequence = watermark.flatten()
        
        return bit_sequence
