"""Translation for NewsBot 2.0 (Module C). Uses deep-translator (no API key needed)."""


class Translator:
    def __init__(self, target="en"):
        self.target = target

    def translate(self, text, target=None):
        try:
            from deep_translator import GoogleTranslator
        except ImportError as e:
            raise ImportError("Install `deep-translator` to use translation.") from e
        return GoogleTranslator(source="auto", target=target or self.target).translate((text or "")[:4900])
