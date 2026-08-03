"""Cross-language analysis for NewsBot 2.0 (Module C).

Detects language, translates non-English articles to English, then the standard
pipeline can analyze them uniformly.
"""
from src.multilingual.translator import Translator
from src.multilingual.language_detector import LanguageDetector


class CrossLingualAnalyzer:
    def __init__(self, translator=None, detector=None):
        self.translator = translator or Translator()
        self.detector = detector or LanguageDetector()

    def to_english(self, text):
        lang = self.detector.detect(text)
        if lang == "en":
            return {"language": lang, "translated": False, "text": text}
        return {"language": lang, "translated": True, "text": self.translator.translate(text, target="en")}
