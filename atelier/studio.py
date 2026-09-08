import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter

class MotorAudioPro:
    def __init__(self, ruta_audio):
        self.sr, self.audio = wav.read(ruta_audio)
        if len(self.audio.shape) > 1:
            self.audio = np.mean(self.audio, axis=1)
        self.audio_norm = self.audio / np.max(np.abs(self.audio))

    def filtro_paso_banda(self, lowcut=80, highcut=15000, order=5):
        nyq = 0.5 * self.sr
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return lfilter(b, a, self.audio_norm)

    def compresor_dinamico(self, audio_input, threshold=0.3, ratio=4.0):
        audio_comprimido = np.copy(audio_input)
        for i, muestra in enumerate(audio_input):
            abs_m = abs(muestra)
            if abs_m > threshold:
                exceso = abs_m - threshold
                nuevo_abs_m = threshold + (exceso / ratio)
                audio_comprimido[i] = np.sign(muestra) * nuevo_abs_m
        return audio_comprimido

    def efecto_reverb(self, audio_input, retraso_ms=50, decaimiento=0.4):
        muestras_retraso = int((retraso_ms / 1000.0) * self.sr)
        reverb_audio = np.zeros(len(audio_input) + muestras_retraso)
        reverb_audio[:len(audio_input)] += audio_input
        reverb_audio[muestras_retraso:] += audio_input * decaimiento
        return reverb_audio[:len(audio_input)]

    def masterizar_pista(self, ruta_salida="master_final.wav"):
        pista_limpia = self.filtro_paso_banda()
        pista_comprimida = self.compresor_dinamico(pista_limpia)
        pista_final = self.efecto_reverb(pista_comprimida)
        audio_final_16bit = np.int16(pista_final * 32767)
        wav.write(ruta_salida, self.sr, audio_final_16bit)
        return ruta_salida
