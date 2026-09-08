import os

class VoiceGate:
    def __init__(self):
        # Mapeo exacto alineado con las opciones del selectbox de Streamlit
        self.acentos = {
            "masculino": {
                "Español (Chile) - Coa / Flaite Urbano": "es-CL-LorenzoNeural",
                "Español (Chile) - Neutro Chileno": "es-CL-LorenzoNeural",
                "Español (Latinoamérica) - Neutro Internacional": "es-MX-JorgeNeural",
                "Español (Castellano - España)": "es-ES-AlvaroNeural",
                "Inglés (EE.UU. - Hip-Hop Studio)": "en-US-ChristopherNeural",
                "Inglés (Reino Unido - London Drill)": "en-GB-RyanNeural"
            },
            "femenino": {
                "Español (Chile) - Coa / Flaite Urbano": "es-CL-CatalinaNeural",
                "Español (Chile) - Neutro Chileno": "es-CL-CatalinaNeural",
                "Español (Latinoamérica) - Neutro Internacional": "es-MX-DaliaNeural",
                "Español (Castellano - España)": "es-ES-ElviraNeural",
                "Inglés (EE.UU. - Hip-Hop Studio)": "en-US-JennyNeural",
                "Inglés (Reino Unido - London Drill)": "en-GB-SoniaNeural"
            }
        }
        # Garantizar existencia del directorio de caché
        os.makedirs("audio_cache", exist_ok=True)

    def obtener_configuracion_voz(self, genero, acento_seleccionado):
        """
        Interpreta el género ingresado y retorna el identificador del modelo exacto.
        """
        genero_key = "masculino" if "male" in genero.lower() else "femenino"
        
        if genero_key in self.acentos:
            return self.acentos[genero_key].get(
                acento_seleccionado, 
                self.acentos[genero_key]["Español (Chile) - Neutro Chileno"]
            )
        return "es-CL-CatalinaNeural"

    def procesar_texto_a_voz(self, texto, modelo_voz):
        """
        Ruta del motor de voz. Muestra logs y retorna la ubicación del archivo.
        """
        ruta_salida = "audio_cache/voz_generada.wav"
        print(f"🗣️ Generando síntesis con el modelo: {modelo_voz}")
        return ruta_salida
