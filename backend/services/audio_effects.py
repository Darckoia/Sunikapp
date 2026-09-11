"""
Audio Effects Service
Handles audio processing effects like reverb, delay, EQ, etc.
"""

import numpy as np
from scipy import signal
from typing import Optional

class AudioEffectsService:
    """Service for audio effects processing"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
    
    def apply_reverb(self, audio: np.ndarray, decay: float = 0.5, delay: float = 0.05) -> np.ndarray:
        """
        Apply simple reverb effect
        
        Args:
            audio: Input audio data
            decay: Decay factor (0-1)
            delay: Delay in seconds
            
        Returns:
            Reverberated audio
        """
        delay_samples = int(delay * self.sample_rate)
        delayed = np.zeros(len(audio) + delay_samples)
        delayed[:len(audio)] = audio
        delayed[delay_samples:] += audio * decay
        return delayed[:len(audio)]
    
    def apply_delay(self, audio: np.ndarray, delay_time: float, feedback: float = 0.5, 
                   wet: float = 0.5) -> np.ndarray:
        """
        Apply delay effect
        
        Args:
            audio: Input audio data
            delay_time: Delay time in seconds
            feedback: Feedback amount (0-1)
            wet: Wet/dry balance (0-1)
            
        Returns:
            Delayed audio
        """
        delay_samples = int(delay_time * self.sample_rate)
        output = np.zeros(len(audio) + delay_samples)
        output[:len(audio)] = audio * (1 - wet)
        output[delay_samples:len(audio) + delay_samples] += audio * wet
        return output[:len(audio)]
    
    def apply_eq(self, audio: np.ndarray, frequencies: list, gains: list, 
                q: float = 1.0) -> np.ndarray:
        """
        Apply parametric EQ
        
        Args:
            audio: Input audio data
            frequencies: List of center frequencies
            gains: List of gains in dB
            q: Q factor
            
        Returns:
            EQ'd audio
        """
        output = audio.copy()
        for freq, gain in zip(frequencies, gains):
            # Simple peak EQ using second-order Butterworth
            if gain != 0:
                sos = signal.iirpeak(freq, q, fs=self.sample_rate)
                output = signal.sosfilt(sos, output)
        return output
    
    def apply_compression(self, audio: np.ndarray, threshold: float = 0.5, 
                         ratio: float = 4.0, attack: float = 0.005, 
                         release: float = 0.1) -> np.ndarray:
        """
        Apply dynamic range compression
        
        Args:
            audio: Input audio data
            threshold: Threshold level
            ratio: Compression ratio
            attack: Attack time in seconds
            release: Release time in seconds
            
        Returns:
            Compressed audio
        """
        output = np.zeros_like(audio)
        attack_samples = int(attack * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        for i in range(len(audio)):
            if abs(audio[i]) > threshold:
                reduction = (abs(audio[i]) - threshold) / (ratio - 1)
                output[i] = np.sign(audio[i]) * (abs(audio[i]) - reduction)
            else:
                output[i] = audio[i]
        
        return output

# Create singleton instance
audio_effects_service = AudioEffectsService()
