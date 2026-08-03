"""Central configuration for NewsBot 2.0.

Keep all tunable parameters and paths here so the rest of the codebase stays clean.
"""
from pathlib import Path

# ---- Paths -----------------------------------------------------------------
ROOT_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = ROOT_DIR / "data"
RAW_DIR     = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR  = DATA_DIR / "models"
RESULTS_DIR = DATA_DIR / "results"
DEFAULT_DATASET = RAW_DIR / "newsbot_bbc.csv"

# ---- Reproducibility -------------------------------------------------------
RANDOM_STATE = 42

# ---- Feature extraction ----------------------------------------------------
MAX_FEATURES = 5000
NGRAM_RANGE  = (1, 2)
MIN_DF = 5
MAX_DF = 0.9

# ---- Classification --------------------------------------------------------
TEST_SIZE = 0.2
UNCERTAIN_MIN_TERMS = 2       # below this many recognized terms -> "uncertain"
UNCERTAIN_MIN_CONFIDENCE = 0.35

# ---- Topic modeling --------------------------------------------------------
N_TOPICS = 5
TOPIC_METHOD = "lda"          # "lda" or "nmf"

# ---- Linguistic sampling (spaCy is the expensive step) ---------------------
LINGUISTIC_SAMPLE_PER_CLASS = 150

# ---- Models ----------------------------------------------------------------
SPACY_MODEL = "en_core_web_sm"
SUMMARIZER_MODEL = "sshleifer/distilbart-cnn-12-6"      # Module B (summarization)
EMBEDDING_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"  # Module B (semantic search)

CATEGORIES = ["business", "entertainment", "politics", "sport", "tech"]
