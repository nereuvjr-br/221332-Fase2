import os

import nltk
import spacy
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

for package in ("wordnet", "omw-1.4", "punkt", "punkt_tab"):
    nltk.download(package, quiet=True)


def load_spacy_model():
    model_name = os.getenv("SPACY_MODEL", "en_core_web_sm")
    try:
        return spacy.load(model_name)
    except OSError as exc:
        raise RuntimeError(
            f"Modelo spaCy '{model_name}' nao encontrado. Execute "
            f"'python -m spacy download {model_name}'."
        ) from exc


nlp = load_spacy_model()

corpus = [
    "cloud computing is scalable",
    "AI is transforming cloud services",
]

vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)


def process_pipeline(text: str) -> dict:
    """Executa o pipeline de NLP usado pela API."""
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text)
    stems = [stemmer.stem(token) for token in tokens]
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    doc = nlp(text)
    pos_tags = [
        {
            "token": token.text,
            "pos": token.pos_,
            "dep": token.dep_,
            "head": token.head.text,
        }
        for token in doc
    ]
    tokens_spacy = [token.text for token in doc]

    matrix = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    vector = dict(zip(feature_names, [round(value, 4) for value in matrix.toarray()[0]]))

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.1:
        sentimento = "Positivo"
    elif polarity < -0.1:
        sentimento = "Negativo"
    else:
        sentimento = "Neutro"

    return {
        "texto_original": text,
        "tokens_nltk": tokens,
        "stems": stems,
        "lemmas": lemmas,
        "pos_tags": pos_tags,
        "tokens_spacy": tokens_spacy,
        "vetor_tfidf": vector,
        "sentimento": {
            "classificacao": sentimento,
            "polaridade": round(polarity, 4),
            "subjetividade": round(subjectivity, 4),
        },
    }


if __name__ == "__main__":
    import json

    resultado = process_pipeline("The new API is amazing")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
