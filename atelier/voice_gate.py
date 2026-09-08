class VoiceGate:
    def __init__(self):
        # Base de datos fonética para inyectar modismos, tonos y variantes de diccionarios
        self.acentos = {
            "masculino": {
                "Español (Chile) - Coa / Flaite Urbano": {
                    "modelo_base": "es-CL-Male-Neural",
                    "diccionario_jerga": ["hermano", "wa", "vio", "voh", "choro", "shispa", "perkin", "waa"],
                    "entrenamiento_estilo": "street_urban_cl"
                },
                "Español (Chile) - Neutro Chileno": {
                    "modelo_base": "es-CL-Male-Neural",
                    "diccionario_jerga": [],
                    "entrenamiento_estilo": "broadcast_neutral_cl"
                },
                "Español (Latinoamérica) - Neutro Internacional": {
                    "modelo_base": "es-MX-Male-Neural",
                    "diccionario_jerga": [],
                    "entrenamiento_estilo": "global_latam"
                },
                "Español (Castellano - España)": {
                    "modelo_base": "es-ES-Male-Neural",
                    "diccionario_jerga": [],
                    "entrenamiento_estilo": "iberic_studio"
                }
            },
            "femenino": {
                "Español (Chile) - Coa / Flaite Urbano": {
                    "modelo_base": "es-CL-Female-Neural",
                    "diccionario_jerga": ["hermana", "wa", "vio", "voh", "perkina"],
                    "entrenamiento_estilo": "street_urban_cl"
                },
                "Español (Chile) - Neutro Chileno": {
                    "modelo_base": "es-CL-Female-Neural",
                    "diccionario_jerga": [],
                    "entrenamiento_estilo": "broadcast_neutral_cl"
                },
                "Español (Latinoamérica) - Neutro Internacional": {
                    "modelo_base": "es-MX-Female-Neural",
                    "diccionario_jerga": [],
                    "entrenamiento_estilo": "global_latam"
                }
            }
        }

    def obtener_configuracion_voz(self, genero, acento_seleccionado):
        """
        Retorna los parámetros de entrenamiento neural exactos 
        según el género y el dialecto específico seleccionado en la consola.
        """
        genero_key = "masculino" if "masculino" in genero.lower() else "femenino"
        
        if genero_key in self.acentos:
            # Busca la configuración o devuelve el Neutro Chileno como respaldo seguro
            return self.acentos[genero_key].get(
                acento_seleccionado, 
                self.acentos[genero_key]["Español (Chile) - Neutro Chileno"]
            )
        return self.acentos["masculino"]["Español (Chile) - Neutro Chileno"]

    def emular_voz_estilo(self, texto, configuracion):
        """
        Simula el procesamiento fonético donde se inyectan las entonaciones 
        urbanas o neutras antes de enviarlo al sintetizador final.
        """
        estilo = configuracion["entrenamiento_estilo"]
        modelo = configuracion["modelo_base"]
        
        print(f"🎙️ [VOICE GATE] Aplicando estilo fonético: '{estilo}' en modelo {modelo}")
        if estilo == "street_urban_cl":
            print("🔥 Modulando frecuencias: Entonación alta al final de las frases y fricción en consonantes S/CH.")
            
        return f"audio_cache/output_{estilo}.wav"
