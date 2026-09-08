from __future__ import annotations

import re

from .models import SongSpec


class Orchestrator:
    """Convierte un prompt de usuario en una especificación estructurada.

    Esta versión es LOCAL/DEMO: no pretende ser un modelo de IA externo.
    """

    def build_song_spec(self, prompt: str) -> SongSpec:
        prompt = prompt.strip()

        if not prompt:
            prompt = "Crear una canción demo"

        return SongSpec(
            title=self._extract_title(prompt),
            genre=self._extract_genre(prompt),
            subgenre=self._extract_subgenre(prompt),
            language=self._extract_language(prompt),
            bpm=self._extract_bpm(prompt),
            key=self._extract_key(prompt),
            duration_seconds=self._extract_duration(prompt),
            structure=self._default_structure(),
            instruments=self._extract_instruments(prompt),
            vocal_style=self._extract_vocal_style(prompt),
            lyrics="",
            production_instructions=prompt,
            original_prompt=prompt,
        )

    def _extract_title(self, prompt: str) -> str:
        match = re.search(
            r"(?:título|titulo|title)\s*[:=-]\s*['\"]?([^'\"]+)",
            prompt,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

        return "Sunikflow Demo"

    def _extract_genre(self, prompt: str) -> str:
        genres = [
            "reggaeton",
            "reggaetón",
            "trap",
            "rap",
            "hip hop",
            "hip-hop",
            "pop",
            "rock",
            "balada",
            "electrónica",
            "electronica",
            "house",
            "techno",
            "drill",
            "cumbia",
            "salsa",
            "bachata",
            "r&b",
        ]

        prompt_lower = prompt.lower()

        for genre in genres:
            if genre in prompt_lower:
                return genre

        return "Unknown"

    def _extract_subgenre(self, prompt: str) -> str:
        subgenres = [
            "reggaeton chileno",
            "reggaetón chileno",
            "trap chileno",
            "latin trap",
            "trap latino",
            "chilean drill",
            "drill chileno",
            "urbano latino",
            "pop urbano",
        ]

        prompt_lower = prompt.lower()

        for subgenre in subgenres:
            if subgenre in prompt_lower:
                return subgenre

        return ""

    def _extract_language(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if any(
            word in prompt_lower
            for word in ["inglés", "ingles", "english"]
        ):
            return "en"

        if any(
            word in prompt_lower
            for word in ["portugués", "portugues", "portuguese"]
        ):
            return "pt"

        if any(
            word in prompt_lower
            for word in ["francés", "frances", "french"]
        ):
            return "fr"

        return "es"

    def _extract_bpm(self, prompt: str) -> int:
        match = re.search(
            r"\b(\d{2,3})\s*(?:bpm|beats?\s*per\s*minute)\b",
            prompt,
            re.IGNORECASE,
        )

        if match:
            return max(40, min(int(match.group(1)), 240))

        return 100

    def _extract_key(self, prompt: str) -> str:
        match = re.search(
            r"\b(?:tono|tonalidad|key)\s*[:=-]?\s*"
            r"([A-G](?:#|b)?(?:m|maj|min)?\b)",
            prompt,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return "C"

    def _extract_duration(self, prompt: str) -> float:
        match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:segundos?|secs?|s)\b",
            prompt,
            re.IGNORECASE,
        )

        if match:
            return max(5.0, min(float(match.group(1)), 900.0))

        match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:minutos|min|m)\b",
            prompt,
            re.IGNORECASE,
        )

        if match:
            minutes = float(match.group(1))
            return max(5.0, min(minutes * 60, 900.0))

        return 180.0

    def _default_structure(self) -> list[str]:
        return [
            "intro",
            "verse",
            "chorus",
            "verse",
            "chorus",
            "bridge",
            "chorus",
            "outro",
        ]

    def _extract_instruments(self, prompt: str) -> list[str]:
        instruments = [
            "piano",
            "guitarra",
            "guitar",
            "bajo",
            "bass",
            "sintetizador",
            "synth",
            "drums",
            "batería",
            "percusión",
            "percussion",
            "pads",
            "strings",
            "cuerdas",
            "808",
            "kick",
            "snare",
            "hi-hat",
            "hihat",
        ]

        prompt_lower = prompt.lower()

        return [
            instrument
            for instrument in instruments
            if instrument in prompt_lower
        ]

    def _extract_vocal_style(self, prompt: str) -> str:
        styles = [
            "melódica",
            "melodica",
            "melódico",
            "melodico",
            "agresiva",
            "agresivo",
            "relajada",
            "relajado",
            "suave",
            "oscura",
            "oscuro",
            "rap",
            "cantado",
            "spoken",
            "susurrado",
        ]

        prompt_lower = prompt.lower()

        found = [
            style
            for style in styles
            if style in prompt_lower
        ]

        return ", ".join(found)


orchestrator = Orchestrator()
