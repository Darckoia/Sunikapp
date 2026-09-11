"""
Audio Mixer Service
Handles mixing and combining multiple audio tracks
"""

import numpy as np
from typing import List, Optional

class MixerService:
    """Service for mixing audio tracks"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def mix_tracks(self, tracks: List[np.ndarray], volumes: Optional[List[float]] = None,
                   pan: Optional[List[float]] = None) -> np.ndarray:
        """
        Mix multiple audio tracks
        
        Args:
            tracks: List of audio arrays
            volumes: List of volume levels (0-1) for each track
            pan: List of pan values (-1 to 1) for each track
            
        Returns:
            Mixed audio
        """
        if not tracks:
            return np.array([])
        
        # Find max length
        max_length = max(len(track) for track in tracks)
        mixed = np.zeros(max_length)
        
        if volumes is None:
            volumes = [1.0] * len(tracks)
        
        if pan is None:
            pan = [0.0] * len(tracks)
        
        for track, volume, pan_value in zip(tracks, volumes, pan):
            padded = np.zeros(max_length)
            padded[:len(track)] = track * volume
            mixed += padded
        
        # Normalize if clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / max_val
        
        return mixed
    
    def adjust_volume(self, audio: np.ndarray, volume_db: float) -> np.ndarray:
        """
        Adjust volume in dB
        
        Args:
            audio: Input audio
            volume_db: Volume adjustment in dB
            
        Returns:
            Volume-adjusted audio
        """
        linear_volume = 10 ** (volume_db / 20.0)
        return audio * linear_volume

# Create singleton instance
mixer_service = MixerService()
