import os
from typing import Dict, List


STYLE_PRESETS: List[Dict[str, object]] = [
    {
        "id": "chileno-neutro",
        "name": "Chileno neutro",
        "aliases": ["chile", "chileno", "neutro", "neutral chileno"],
        "tags": ["Chile", "español chileno", "pop latino", "voz clara"],
        "prompt": "Pop latino contemporáneo desde Chile, ritmo medio, bajo cálido, guitarra limpia, producción natural y voz clara en español chileno neutro",
        "bpm": 96,
        "energy": 0.58,
    },
    {
        "id": "flaite-urbano",
        "name": "Urbano CL / Coa",
        "aliases": ["flaite", "coa", "urbano cl", "urbano chileno", "trap chileno"],
        "tags": ["Chile", "urbano", "trap", "reggaetón", "street"],
        "prompt": "Urbano chileno actual, 808 profundo, hi-hats rápidos, percusión seca, sintetizadores oscuros y entrega vocal callejera sin caricaturas",
        "bpm": 94,
        "energy": 0.82,
    },
    {
        "id": "reggaeton-cl",
        "name": "Reggaetón chileno",
        "aliases": ["reggaeton", "reggaetón", "perreo"],
        "tags": ["Chile", "reggaetón", "latino", "bailable"],
        "prompt": "Reggaetón latino con acento chileno, dembow firme, bajo 808, sintetizadores brillantes y coro pegajoso",
        "bpm": 96,
        "energy": 0.86,
    },
    {
        "id": "trap-santiago",
        "name": "Trap Santiago",
        "aliases": ["trap", "santiago", "drill cl"],
        "tags": ["Chile", "trap", "808", "oscuro"],
        "prompt": "Trap nocturno de Santiago, 808 distorsionado, pads sombríos, caja crujiente y flow preciso",
        "bpm": 140,
        "energy": 0.78,
    },
    {
        "id": "cumbia-chilena",
        "id": "cumbia-chilena",
        "name": "Cumbia chilena",
        "aliases": ["cumbia", "tropical", "chilena tropical"],
        "tags": ["Chile", "cumbia", "tropical", "acordeón"],
        "prompt": "Cumbia chilena luminosa, acordeón melódico, güira, bajo bailable y coro festivo",
        "bpm": 102,
        "energy": 0.74,
    },
    {
        "id": "synth-pop",
        "name": "Synth pop",
        "aliases": ["synth", "synthpop", "electropop"],
        "tags": ["synth pop", "electrónico", "nostálgico"],
        "prompt": "Synth pop emocional, arpegios analógicos, bombo profundo, coros amplios y producción cinematográfica",
        "bpm": 108,
        "energy": 0.68,
    },
    {
        "id": "hip-hop-latam",
        "name": "Hip-hop latino",
        "aliases": ["hip hop", "rap", "latam"],
        "tags": ["hip-hop", "rap", "latino", "boom bap"],
        "prompt": "Hip-hop latino con boom bap moderno, bajo redondo, samples cálidos y voz rítmica en español",
        "bpm": 90,
        "energy": 0.64,
    },
    {
        "id": "drill-uk",
        "name": "Drill UK",
        "aliases": ["drill", "uk drill", "london"],
        "tags": ["drill", "Reino Unido", "oscuro", "808"],
        "prompt": "UK drill oscuro, 808 deslizante, hi-hats sincopados, cuerdas tensas y entrega vocal contenida",
        "bpm": 142,
        "energy": 0.8,
    },
]

VOICE_PROFILES: List[Dict[str, object]] = [
    {"id": "cl-catalina-neutral", "name": "Catalina - Chile neutro", "language": "es", "language_name": "Español", "locale": "es-CL", "gender": "female", "style": "neutral", "provider_voice": "es-CL-CatalinaNeural", "description": "Voz femenina chilena clara y natural"},
    {"id": "cl-lorenzo-neutral", "name": "Lorenzo - Chile neutro", "language": "es", "language_name": "Español", "locale": "es-CL", "gender": "male", "style": "neutral", "provider_voice": "es-CL-LorenzoNeural", "description": "Voz masculina chilena clara y natural"},
    {"id": "cl-catalina-urbana", "name": "Catalina - Urbano CL", "language": "es", "language_name": "Español", "locale": "es-CL", "gender": "female", "style": "urbano", "provider_voice": "es-CL-CatalinaNeural", "description": "Voz femenina chilena para estilos urbanos"},
    {"id": "cl-lorenzo-urbano", "name": "Lorenzo - Urbano CL", "language": "es", "language_name": "Español", "locale": "es-CL", "gender": "male", "style": "urbano", "provider_voice": "es-CL-LorenzoNeural", "description": "Voz masculina chilena para estilos urbanos"},
    {"id": "latam-dalia", "name": "Dalia - Latinoamérica", "language": "es", "language_name": "Español", "locale": "es-MX", "gender": "female", "style": "neutral", "provider_voice": "es-MX-DaliaNeural", "description": "Español latinoamericano neutro"},
    {"id": "latam-jorge", "name": "Jorge - Latinoamérica", "language": "es", "language_name": "Español", "locale": "es-MX", "gender": "male", "style": "neutral", "provider_voice": "es-MX-JorgeNeural", "description": "Español latinoamericano neutro"},
    {"id": "spain-elvira", "name": "Elvira - España", "language": "es", "language_name": "Español", "locale": "es-ES", "gender": "female", "style": "neutral", "provider_voice": "es-ES-ElviraNeural", "description": "Castellano de España"},
    {"id": "spain-alvaro", "name": "Álvaro - España", "language": "es", "language_name": "Español", "locale": "es-ES", "gender": "male", "style": "neutral", "provider_voice": "es-ES-AlvaroNeural", "description": "Castellano de España"},
    {"id": "en-us-jenny", "name": "Jenny - English US", "language": "en", "language_name": "English", "locale": "en-US", "gender": "female", "style": "neutral", "provider_voice": "en-US-JennyNeural", "description": "English voice for pop and studio vocals"},
    {"id": "en-us-christopher", "name": "Christopher - English US", "language": "en", "language_name": "English", "locale": "en-US", "gender": "male", "style": "urban", "provider_voice": "en-US-ChristopherNeural", "description": "English voice for hip-hop and urban production"},
    {"id": "en-gb-sonia", "name": "Sonia - English UK", "language": "en", "language_name": "English", "locale": "en-GB", "gender": "female", "style": "neutral", "provider_voice": "en-GB-SoniaNeural", "description": "British English voice"},
    {"id": "en-gb-ryan", "name": "Ryan - English UK", "language": "en", "language_name": "English", "locale": "en-GB", "gender": "male", "style": "urban", "provider_voice": "en-GB-RyanNeural", "description": "British English voice for drill and urban styles"},
    {"id": "fr-fr-denise", "name": "Denise - Français", "language": "fr", "language_name": "Français", "locale": "fr-FR", "gender": "female", "style": "neutral", "provider_voice": "fr-FR-DeniseNeural", "description": "Voix française naturelle"},
    {"id": "de-de-conrad", "name": "Conrad - Deutsch", "language": "de", "language_name": "Deutsch", "locale": "de-DE", "gender": "male", "style": "neutral", "provider_voice": "de-DE-ConradNeural", "description": "Deutsche Stimme"},
    {"id": "pt-br-francisca", "name": "Francisca - Português BR", "language": "pt", "language_name": "Português", "locale": "pt-BR", "gender": "female", "style": "neutral", "provider_voice": "pt-BR-FranciscaNeural", "description": "Voz brasileira natural"},
    {"id": "it-it-elsa", "name": "Elsa - Italiano", "language": "it", "language_name": "Italiano", "locale": "it-IT", "gender": "female", "style": "neutral", "provider_voice": "it-IT-ElsaNeural", "description": "Voce italiana naturale"},
    {"id": "ja-jp-nanami", "name": "Nanami - 日本語", "language": "ja", "language_name": "日本語", "locale": "ja-JP", "gender": "female", "style": "neutral", "provider_voice": "ja-JP-NanamiNeural", "description": "Natural Japanese voice"},
    {"id": "ko-kr-sunhi", "name": "Sun-Hi - 한국어", "language": "ko", "language_name": "한국어", "locale": "ko-KR", "gender": "female", "style": "neutral", "provider_voice": "ko-KR-SunHiNeural", "description": "Natural Korean voice"},
]

SOUND_EFFECTS: List[Dict[str, object]] = [
    {"id": "thunder", "name": "Trueno", "default_duration": 2.5, "description": "Retumbo grave con caída atmosférica"},
    {"id": "rain", "name": "Lluvia", "default_duration": 4.0, "description": "Lluvia constante con textura suave"},
    {"id": "gunshot", "name": "Disparo", "default_duration": 0.45, "description": "Impacto percusivo seco para montaje"},
    {"id": "crowd", "name": "Multitud", "default_duration": 2.0, "description": "Ambiencia de público a distancia"},
    {"id": "siren", "name": "Sirena", "default_duration": 2.0, "description": "Barrido de sirena cinematográfico"},
    {"id": "vinyl", "name": "Vinilo", "default_duration": 3.0, "description": "Ruido analógico y crackle suave"},
    {"id": "door", "name": "Portazo", "default_duration": 0.6, "description": "Golpe grave con cola corta"},
]


class VoiceGate:
    def __init__(self):
        self.acentos = {
            "masculino": {profile["name"]: profile["provider_voice"] for profile in VOICE_PROFILES if profile["gender"] == "male"},
            "femenino": {profile["name"]: profile["provider_voice"] for profile in VOICE_PROFILES if profile["gender"] == "female"},
        }
        os.makedirs("audio_cache", exist_ok=True)

    def listar_estilos(self) -> List[Dict[str, object]]:
        return STYLE_PRESETS

    def listar_voces(self) -> List[Dict[str, object]]:
        return VOICE_PROFILES

    def listar_efectos(self) -> List[Dict[str, object]]:
        return SOUND_EFFECTS

    def resolver_estilo(self, style_ids=None, prompt=""):
        styles = list(style_ids or [])
        if styles:
            selected = [style for style in STYLE_PRESETS if style["id"] in styles]
            if selected:
                return selected
        text = f"{prompt} ".lower()
        matched = []
        for style in STYLE_PRESETS:
            aliases = [str(alias).lower() for alias in style.get("aliases", [])]
            if any(alias in text for alias in aliases):
                matched.append(style)
        return matched or [STYLE_PRESETS[0]]

    def resolver_voz(self, voice_id=None, language="es", gender="female", style=None):
        profiles = [profile for profile in VOICE_PROFILES if profile["language"] == language]
        if style == "urbano":
            profiles = [profile for profile in profiles if profile.get("style") == "urbano"] or profiles
        if gender in {"male", "female"}:
            gender_profiles = [profile for profile in profiles if profile["gender"] == gender]
            if gender_profiles:
                profiles = gender_profiles
        if voice_id:
            for profile in VOICE_PROFILES:
                if profile["id"] == voice_id or profile["provider_voice"] == voice_id:
                    return profile
        return profiles[0] if profiles else VOICE_PROFILES[0]

    def obtener_configuracion_voz(self, genero, acento_seleccionado):
        genero_key = "masculino" if "male" in genero.lower() else "femenino"
        return self.acentos.get(genero_key, {}).get(
            acento_seleccionado,
            "es-CL-CatalinaNeural",
        )

    def procesar_texto_a_voz(self, texto, modelo_voz):
        ruta_salida = "audio_cache/voz_generada.wav"
        return ruta_salida
