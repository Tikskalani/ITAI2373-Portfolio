"""Language detection for NewsBot 2.0 (Module C)."""


class LanguageDetector:
    def detect(self, text):
        try:
            from langdetect import detect
        except ImportError as e:
            raise ImportError("Install `langdetect` to use language detection.") from e
        try:
            return detect(text)
        except Exception:
            return "unknown"
