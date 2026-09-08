import streamlit as st
import requests

class VoiceGate:
    def __init__(self):
        # Intentar extraer la llave segura que guardaste en los Secrets de Streamlit
        self.api_key = st.secrets.get("ELEVENLABS_API_KEY", "")
        
        # Mapeo de IDs de modelos de voz pre-entrenados para el ecosistema S_FLOW
        # (Se usan IDs estándar estables de ElevenLabs; puedes cambiarlos por clones propios)
        self.acentos = {
            "masculino": {
                "Español (Chile) - Coa / Flaite Urbano": {
                    "voice_id": "pNInz6obpgfr9ff95uU0", # ID de respaldo (Latam) hasta subir tu clon flaite
                    "stability": 0.35,
                    "similarity": 0.85
                },
                "Español (Chile) - Neutro Chileno": {
                    "voice_id": "pNInz6obpgfr9ff95uU0",
                    "stability": 0.50,
                    "similarity": 0.75
                },
                "Español (Latinoamérica) - Neutro Internacional": {
                    "voice_id": "pNInz6obpgfr9ff95uU0",
                    "stability": 0.45,
                    "similarity": 0.75
                }
            },
            "femenino": {
                "Español (Chile) - Coa / Flaite Urbano": {
                    "voice_id": "EXAVITQu4vr4xnSDxMaL",
                    "stability": 0.35,
                    "similarity": 0.85
                },
                "Español (Chile) - Neutro Chileno": {
                    "voice_id": "EXAVITQu4vr4xnSDxMaL",
                    "stability": 0.50,
                    "similarity": 0.75
                }
            }
        }

    def obtener_configuracion_voz(self, genero, acento_seleccionado):
        """ Filtra y extrae los diccionarios de configuración para la consola web """
        genero_key = "masculino" if "male" in genero.lower() or "masculina" in genero.lower() else "femenino"
        if genero_key in self.acentos:
            return self.acentos[genero_key].get(
                acento_seleccionado, 
                self.acentos[genero_key]["Español (Chile) - Neutro Chileno"]
            )
        return {"voice_id": "pNInz6obpgfr9ff95uU0", "stability": 0.45, "similarity": 0.75}

    def generar_voz_por_api_real(self, texto, genero, acento_seleccionado):
        """
        Conexión directa a internet. Envía la lírica a ElevenLabs 
        usando tu token secreto sk_... y descarga el archivo de audio.
        """
        if not self.api_key:
            print("⚠️ [S_FLOW] No se detectó API Key en Secrets. Corriendo en modo simulación.")
            return None
            
        config = self.obtener_configuracion_voz(genero, acento_seleccionado)
        voice_id = config["voice_id"]
        
        url = f"https://elevenlabs.io{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": texto,
            "model_id": "eleven_multilingual_v2", # El mejor modelo para captar modismos del español
            "voice_settings": {
                "stability": config["stability"],
                "similarity_boost": config["similarity"]
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                ruta_salida = "audio_cache/vocal_master_real.mp3"
                with open(ruta_salida, "wb") as f:
                    f.write(response.content)
                return ruta_salida
        except Exception as e:
            print(f"Error llamando a la API de ElevenLabs: {e}")
            
        return None
        
