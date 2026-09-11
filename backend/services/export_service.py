"""
Audio Export Service - Fixed version
Handles exporting audio to WAV and MP3 formats
"""

import numpy as np
from pathlib import Path
from typing import Optional
import wave
import struct
import io

class ExportService:
    """Service for exporting audio files"""
    
    def __init__(self, sample_rate: int = 44100, bit_depth: int = 16):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
    
    def normalize_audio(self, audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
        """
        Normalize audio to target level
        
        Args:
            audio: Audio data to normalize
            target_db: Target level in dB
            
        Returns:
            Normalized audio
        """
        # Calculate RMS level
        rms = np.sqrt(np.mean(audio ** 2))
        if rms == 0:
            return audio
        
        # Calculate gain needed
        target_linear = 10 ** (target_db / 20.0)
        gain = target_linear / rms
        
        return audio * gain
    
    def export_wav(self, audio: np.ndarray, file_path: str, 
                   sample_rate: Optional[int] = None, normalize: bool = True) -> bool:
        """
        Export audio to WAV format
        
        Args:
            audio: Audio data to export (numpy array, values -1.0 to 1.0)
            file_path: Output file path
            sample_rate: Sample rate (uses default if not specified)
            normalize: Whether to normalize audio before export
            
        Returns:
            True if successful, False otherwise
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        
        try:
            # Ensure output directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Normalize if requested
            if normalize:
                audio = self.normalize_audio(audio)
            
            # Convert to int16 (-32768 to 32767)
            # Clip to prevent overflow
            audio_clipped = np.clip(audio, -1.0, 1.0)
            audio_int16 = np.int16(audio_clipped * 32767)
            
            # Write WAV file
            with wave.open(file_path, 'w') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit = 2 bytes
                wav_file.setframerate(int(sample_rate))
                wav_file.writeframes(audio_int16.tobytes())
            
            return True
            
        except Exception as e:
            print(f"Error exporting WAV: {e}")
            return False
    
    def export_wav_stereo(self, audio_left: np.ndarray, audio_right: np.ndarray, 
                         file_path: str, sample_rate: Optional[int] = None, 
                         normalize: bool = True) -> bool:
        """
        Export stereo audio to WAV format
        
        Args:
            audio_left: Left channel audio data
            audio_right: Right channel audio data
            file_path: Output file path
            sample_rate: Sample rate (uses default if not specified)
            normalize: Whether to normalize audio before export
            
        Returns:
            True if successful, False otherwise
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        
        try:
            # Ensure output directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Ensure equal length
            min_len = min(len(audio_left), len(audio_right))
            audio_left = audio_left[:min_len]
            audio_right = audio_right[:min_len]
            
            # Normalize if requested
            if normalize:
                audio_left = self.normalize_audio(audio_left)
                audio_right = self.normalize_audio(audio_right)
            
            # Convert to int16
            audio_left_clipped = np.clip(audio_left, -1.0, 1.0)
            audio_right_clipped = np.clip(audio_right, -1.0, 1.0)
            audio_left_int16 = np.int16(audio_left_clipped * 32767)
            audio_right_int16 = np.int16(audio_right_clipped * 32767)
            
            # Interleave channels
            stereo_data = np.zeros(min_len * 2, dtype=np.int16)
            stereo_data[0::2] = audio_left_int16
            stereo_data[1::2] = audio_right_int16
            
            # Write WAV file
            with wave.open(file_path, 'w') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit = 2 bytes
                wav_file.setframerate(int(sample_rate))
                wav_file.writeframes(stereo_data.tobytes())
            
            return True
            
        except Exception as e:
            print(f"Error exporting stereo WAV: {e}")
            return False
    
    def export_mp3(self, audio: np.ndarray, file_path: str, 
                   sample_rate: Optional[int] = None, bitrate: int = 192,
                   normalize: bool = True) -> bool:
        """
        Export audio to MP3 format (requires pydub)
        
        Args:
            audio: Audio data to export
            file_path: Output file path
            sample_rate: Sample rate (uses default if not specified)
            bitrate: Bitrate in kbps (default 192)
            normalize: Whether to normalize audio before export
            
        Returns:
            True if successful, False otherwise
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        
        try:
            # Import pydub (optional dependency)
            from pydub import AudioSegment
            import io
            
            # Ensure output directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Normalize if requested
            if normalize:
                audio = self.normalize_audio(audio)
            
            # Convert to int16
            audio_clipped = np.clip(audio, -1.0, 1.0)
            audio_int16 = np.int16(audio_clipped * 32767)
            
            # Create temporary WAV in memory
            wav_io = io.BytesIO()
            with wave.open(wav_io, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(int(sample_rate))
                wav_file.writeframes(audio_int16.tobytes())
            
            wav_io.seek(0)
            
            # Convert WAV to MP3 using pydub
            audio_segment = AudioSegment.from_wav(wav_io)
            audio_segment.export(
                file_path,
                format="mp3",
                bitrate=f"{bitrate}k"
            )
            
            return True
            
        except ImportError:
            print("Error: pydub not installed. Install with: pip install pydub")
            print("Note: ffmpeg or libav must also be installed for MP3 support")
            return False
        except Exception as e:
            print(f"Error exporting MP3: {e}")
            return False
    
    def export_flac(self, audio: np.ndarray, file_path: str,
                   sample_rate: Optional[int] = None, normalize: bool = True) -> bool:
        """
        Export audio to FLAC format (lossless)
        
        Args:
            audio: Audio data to export
            file_path: Output file path
            sample_rate: Sample rate (uses default if not specified)
            normalize: Whether to normalize audio before export
            
        Returns:
            True if successful, False otherwise
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        
        try:
            # Import soundfile (optional dependency)
            import soundfile as sf
            
            # Ensure output directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Normalize if requested
            if normalize:
                audio = self.normalize_audio(audio)
            
            # Clip to valid range
            audio = np.clip(audio, -1.0, 1.0)
            
            # Write FLAC file
            sf.write(file_path, audio, int(sample_rate), subtype='PCM_16')
            
            return True
            
        except ImportError:
            print("Error: soundfile not installed. Install with: pip install soundfile")
            return False
        except Exception as e:
            print(f"Error exporting FLAC: {e}")
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
            "duration_seconds": float(duration),
            "duration_formatted": self._format_duration(duration),
            "sample_rate": self.sample_rate,
            "bit_depth": self.bit_depth,
            "total_samples": len(audio),
            "peak_level_db": self._to_db(np.max(np.abs(audio))),
            "rms_level_db": self._to_db(np.sqrt(np.mean(audio ** 2))),
            "channels": 1
        }
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Get information about a WAV file
        
        Args:
            file_path: Path to WAV file
            
        Returns:
            Dictionary with file information or None if error
        """
        try:
            with wave.open(file_path, 'rb') as wav_file:
                n_channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                sample_rate = wav_file.getframerate()
                n_frames = wav_file.getnframes()
                
                duration = n_frames / sample_rate
                
                return {
                    "channels": n_channels,
                    "sample_width": sample_width,
                    "sample_rate": sample_rate,
                    "total_frames": n_frames,
                    "duration_seconds": float(duration),
                    "duration_formatted": self._format_duration(duration),
                    "bit_depth": sample_width * 8,
                    "file_path": file_path
                }
        except Exception as e:
            print(f"Error reading file info: {e}")
            return None
    
    @staticmethod
    def _to_db(linear_value: float) -> float:
        """
        Convert linear amplitude to dB
        
        Args:
            linear_value: Linear amplitude value
            
        Returns:
            Value in dB
        """
        if linear_value <= 0:
            return -np.inf
        return 20 * np.log10(linear_value)
    
    @staticmethod
    def _format_duration(seconds: float) -> str:
        """
        Format duration in seconds to HH:MM:SS
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

# Create singleton instance
export_service = ExportService()
