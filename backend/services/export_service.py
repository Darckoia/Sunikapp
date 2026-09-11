"""
Audio Export Service
Handles exporting audio to various formats
"""

import numpy as np
from pathlib import Path
from typing import Optional
import wave
import struct

class ExportService:
    """Service for exporting audio files"""
    
    def __init__(self, sample_rate: int = 44100, bit_depth: int = 16):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
    
    def export_wav(self, audio: np.ndarray, file_path: str, 
                   sample_rate: Optional[int] = None) -> bool:
        """
        Export audio to WAV format
        
        Args:
            audio: Audio data to export
            file_path: Output file path
            sample_rate: Sample rate (uses default if not specified)
            
        Returns:
            True if successful
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        
        try:
            # Convert to int16
            audio_int = np.int16(audio / np.max(np.abs(audio)) * 32767)
            
            with wave.open(file_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_int.tobytes())
            
            return True
        except Exception as e:
            print(f"Error exporting WAV: {e}")
            return False
    
    def export_raw(self, audio: np.ndarray, file_path: str) -> bool:
        """
        Export raw audio data
        
        Args:
            audio: Audio data to export
            file_path: Output file path
            
        Returns:
            True if successful
        """
        try:
            audio.tofile(file_path)
            return True
        except Exception as e:
            print(f"Error exporting raw: {e}")
            return False
    
    def get_audio_info(self, audio: np.ndarray) -> dict:
        """
        Get information about audio data
        
        Args:
            audio: Audio data
            
        Returns:
            Dictionary with audio information
        """
        duration = len(audio) / self.sample_rate
        return {
            "duration": duration,
            "sample_rate": self.sample_rate,
            "bit_depth": self.bit_depth,
            "samples": len(audio),
            "peak_level": float(np.max(np.abs(audio))),
            "rms_level": float(np.sqrt(np.mean(audio ** 2)))
        }

# Create singleton instance
export_service = ExportService()
