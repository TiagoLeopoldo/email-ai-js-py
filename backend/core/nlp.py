import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Garantir recursos NLTK
def _ensure_nltk_resources():
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

_ensure_nltk_resources()

lemmatizer = WordNetLemmatizer()
try:
    STOP_PT = set(stopwords.words("portuguese"))
except Exception:
    STOP_PT = {"a","o","os","as","de","da","do","das","dos","e","é","em","um","uma","para","por","com","sem","no","na","nos","nas","que","se","sua","seu"}

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ÿ\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> list:
    return text.split()

def remove_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in STOP_PT and len(t) > 1]

def lemmatize_tokens(tokens: list) -> list:
    return [lemmatizer.lemmatize(t) for t in tokens]

def preprocess_text(text: str) -> str:
    norm = normalize_text(text)
    toks = tokenize(norm)
    toks = remove_stopwords(toks)
    toks = lemmatize_tokens(toks)
    processed = " ".join(toks).strip()
    return processed if processed else norm
