"""Sentiment and emotion analysis for NewsBot 2.0."""
import nltk

EMOTION_LEXICON = {
 "anger":        {"angry","rage","fury","outrage","hostile","attack","fight","violence","conflict","threat","clash","dispute","assault"},
 "anticipation": {"expect","await","anticipate","upcoming","future","plan","prepare","forecast","predict","outlook","prospect"},
 "disgust":      {"disgust","sick","gross","revolt","offensive","vile","repulsive","nasty","corrupt","scandal","shameful"},
 "fear":         {"fear","afraid","scared","threat","danger","risk","worry","anxiety","panic","terror","crisis","alarm","concern","warn"},
 "joy":          {"joy","happy","delight","celebrate","win","victory","success","triumph","cheer","glad","pleasure","excited","enjoy","award"},
 "sadness":      {"sad","grief","sorrow","mourn","tragic","loss","defeat","despair","unhappy","disappoint","suffer","death"},
 "surprise":     {"surprise","shock","unexpected","sudden","astonish","amaze","stun","remarkable","dramatic"},
 "trust":        {"trust","confidence","reliable","secure","support","partner","agreement","faith","honest","credible","stable"},
}


def _ensure_vader():
    try:
        nltk.data.find("sentiment/vader_lexicon")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


class SentimentAnalyzer:
    """VADER + TextBlob sentiment with a transparent keyword-based emotion label."""

    def __init__(self):
        _ensure_vader()
        from nltk.sentiment import SentimentIntensityAnalyzer
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> dict:
        from textblob import TextBlob
        comp = self.sia.polarity_scores(text)["compound"]
        tb = TextBlob(text).sentiment
        label = "positive" if comp >= 0.05 else "negative" if comp <= -0.05 else "neutral"
        return {"compound": round(comp, 3), "label": label,
                "polarity": round(tb.polarity, 3), "subjectivity": round(tb.subjectivity, 3),
                "emotion": self.detect_emotion(text)}

    @staticmethod
    def detect_emotion(text: str) -> str:
        toks = set(text.lower().split())
        scores = {e: len(toks & words) for e, words in EMOTION_LEXICON.items()}
        return max(scores, key=scores.get) if sum(scores.values()) > 0 else "neutral"
