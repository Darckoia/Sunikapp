"""
Audio Synthesis Service
Handles core audio generation and synthesis operations
"""

import numpy as np
from typing import Optional, Tuple

class AudioSynthesisService:
    """Service for audio synthesis operations"""
    
    def __init__(self, sample_rate: int = 44100, bit_depth: int = 16):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.duration = 10  # Default 10 seconds
    
    def generate_sine_wave(self, frequency: float, duration: Optional[float] = None) -> np.ndarray:
        """
        Generate a sine wave at the specified frequency
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            
        Returns:
            Audio data as numpy array
        """
        if duration is None:
            duration = self.duration
            
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        waveform = np.sin(2 * np.pi * frequency * t)
        return waveform
    
    def generate_chord(self, frequencies: list, duration: Optional[float] = None) -> np.ndarray:
        """
        Generate a chord (multiple frequencies)
        
        Args:
            frequencies: List of frequencies in Hz
            duration: Duration in seconds
            
        Returns:
            Audio data as numpy array
        """
        if duration is None:
            duration = self.duration
            
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        waveform = np.zeros_like(t)
        
        for freq in frequencies:
            waveform += np.sin(2 * np.pi * freq * t)
        
        # Normalize to prevent clipping
        waveform = waveform / len(frequencies)
        return waveform
    
    def apply_envelope(self, waveform: np.ndarray, attack: float, decay: float, 
                      sustain: float, release: float) -> np.ndarray:
        """
        Apply ADSR envelope to waveform
        
        Args:
            waveform: Input audio data
            attack: Attack time in seconds
            decay: Decay time in seconds
            sustain: Sustain level (0-1)
            release: Release time in seconds
            
        Returns:
            Enveloped audio data
        """
        total_samples = len(waveform)
        envelope = np.ones(total_samples)
        
        # Attack
        attack_samples = int(attack * self.sample_rate)
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        decay_samples = int(decay * self.sample_rate)
        if decay_samples > 0:
            decay_start = attack_samples
            decay_end = decay_start + decay_samples
            envelope[decay_start:decay_end] = np.linspace(1, sustain, decay_samples)
        
        # Release
        release_samples = int(release * self.sample_rate)
        if release_samples > 0:
            release_start = total_samples - release_samples
            envelope[release_start:] = np.linspace(sustain, 0, release_samples)
        
        return waveform * envelope

# Create singleton instance
audio_synth_service = AudioSynthesisService()
