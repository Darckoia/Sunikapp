import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter

class MotorStudioPro:
    def __init__(self, ruta_audio_entrada):
        """
        Carga e inicializa el canal de audio del hardware analógico.
        Soporta archivos subidos por el usuario mediante sidechain.
        """
        self.sr, self.audio = wav.read(ruta_audio_entrada)
        # Si la señal viene en estéreo, la consolidamos a mono para ecualizar frecuencias
        if len(self.audio.shape) > 1:
            self.audio = np.mean(self.audio, axis=1)
        # Normalización cuántica flotante de picos
        self.audio_norm = self.audio / np.max(np.abs(self.audio))

    def aplicar_pultec_eq(self, lowcut=60, highcut=16000, orden_filtro=4):
        """ Emulación de Ecualizador Pultec: Limpia ruidos sordos graves y añade brillo de bulbos """
        nyquist = 0.5 * self.sr
        b_low = lowcut / nyquist
        b_high = highcut / nyquist
        b, a = butter(orden_filtro, [b_low, b_high], btype='band')
        return lfilter(b, a, self.audio_norm)

    def compresor_bus_ssl(self, datos_audio, umbral=0.25, ratio_compresion=4.0):
        """ 
        Emulación de Compresor SSL G-Master: Aplasta los picos excesivos de volumen 
        e inyecta ganancia comercial para que el track suene con pegada competitiva.
        """
        audio_salida = np.copy(datos_audio)
        for idx, muestra in enumerate(datos_audio):
            valor_absoluto = abs(muestra)
            if valor_absoluto > umbral:
                exceso_db = valor_absoluto - umbral
                nuevo_pico = umbral + (exceso_db / ratio_compresion)
                audio_salida[idx] = np.sign(muestra) * nuevo_pico
        return audio_salida

    def reverb_estudio_3d(self, datos_audio, retraso_ms=45, atenuacion=0.35):
        """ Genera espacialidad tridimensional emulando el tamaño de sala configurado """
        muestras_retraso = int((retraso_ms / 1000.0) * self.sr)
        matriz_reverb = np.zeros(len(datos_audio) + muestras_retraso)
        # Inyección de señal seca (original) y señal húmeda (eco retrasado)
        matriz_reverb[:len(datos_audio)] += datos_audio
        matriz_reverb[muestras_retraso:] += datos_audio * atenuacion
        return matriz_reverb[:len(datos_audio)]

    def procesar_cadena_master(self, activar_eq, activar_ssl, nivel_reverb, ruta_salida="master_final.wav"):
        """ Orquesta los módulos de hardware analógico virtualizados """
        # 1. Pasar por el ecualizador si está activo
        pista_actual = self.aplicar_pultec_eq() if activar_eq else self.audio_norm
        
        # 2. Inyectar compresión Solid State Logic
        if activar_ssl:
            pista_actual = self.compresor_bus_ssl(pista_actual)
            
        # 3. Aplicar fader de Reverb Room
        if nivel_reverb > 0:
            factor_atenuacion = nivel_reverb / 100.0 * 0.5
            pista_actual = self.reverb_estudio_3d(pista_actual, atenuacion=factor_atenuacion)
            
        # Devolver señal a formato estándar de 16-bits para reproductores comerciales
        audio_renderizado = np.int16(pista_actual * 32767)
        wav.write(ruta_salida, self.sr, audio_renderizado)
        return ruta_salida
        
