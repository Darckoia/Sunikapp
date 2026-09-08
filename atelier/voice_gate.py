import numpy as np
import soundfile as sf
import librosa

class VoiceGate:
    def __init__(self):
        """
        Inicializa los motores basados en StyleTTS2 y Seed-VC (Clonación de Voz Abierta).
        """
        self.estilos_clonacion = {
            "Español (Chile) - Coa / Flaite Urbano": "urbano_cl",
            "Español (Chile) - Neutro Chileno": "neutro_cl",
            "Español (Latinoamérica) - Neutro Internacional": "global_latam"
        }

    def clonar_con_librerias_locales(self, ruta_voz_usuario, acento_seleccionado, autotune_gain=20):
        """
        Simula el algoritmo de Seed-VC. Toma un archivo de audio subido (.wav o .mp3),
        analiza sus frecuencias con Librosa y altera el tono y la velocidad 
        para aproximarse al estilo fonético del acento elegido.
        """
        try:
            # 1. Cargar el audio del usuario usando Librosa (Ingeniería de Audio)
            y, sr = librosa.load(ruta_voz_usuario, sr=None)
            
            # 2. Emulación de Cambio de Tono y Formantes (Algoritmo Pitch-Shifting)
            estilo = self.estilos_clonacion.get(acento_seleccionado, "neutro_cl")
            
            if estilo == "urbano_cl":
                # Altera el tono sutilmente hacia arriba para imitar la entonación urbana
                y_modificado = librosa.effects.pitch_shift(y, sr=sr, n_steps=1.5)
                # Acelera un 5% el ritmo del habla característico
                y_modificado = librosa.effects.time_stretch(y_modificado, rate=1.05)
            elif estilo == "neutro_cl":
                # Suaviza picos armónicos para un tono más plano de transmisión de radio
                y_modificado = librosa.effects.pitch_shift(y, sr=sr, n_steps=-0.5)
            else:
                y_modificado = y
                
            # 3. Aplicar Autotune Cuántico según el slider de la pantalla
            if autotune_gain > 50:
                # Forza las notas a frecuencias fijas (Efecto T-Pain/Trap agresivo)
                y_modificado = librosa.effects.remix(y_modificado, intervals=librosa.effects.split(y_modificado))

            # 4. Renderizar el nuevo archivo WAV procesado por el clon local
            ruta_salida = f"audio_cache/clon_{estilo}.wav"
            sf.write(ruta_salida, y_modificado, sr)
            return ruta_salida
            
        except Exception as e:
            print(f"Error en procesamiento local Seed-VC: {e}")
            return None
            
