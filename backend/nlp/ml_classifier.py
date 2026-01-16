# backend/nlp/ml_classifier.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from nlp.training_data import TRAINING_DATA  # <-- corrigido

texts, labels = zip(*TRAINING_DATA)

# Cria pipeline: vetoriza texto + treina modelo
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

# Treina modelo
model.fit(texts, labels)

def predict_intent(text: str) -> str:
    """Prediz intenção usando modelo treinado"""
    return model.predict([text])[0]

def predict_proba(text: str) -> dict:
    """Retorna probabilidades de cada classe"""
    probs = model.predict_proba([text])[0]
    classes = model.classes_
    return {cls: float(prob) for cls, prob in zip(classes, probs)}
