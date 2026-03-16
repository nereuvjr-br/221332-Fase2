# imports para técnicas de morfologia 
import spacy
import nltk

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Análise de sentimento léxica 
from textblob import TextBlob

# Vetorização 
from sklearn.feature_extraction.text import TfidfVectorizer

# Imports para técnicas de sintaxe 
import spacy

# Carrega modelo spaCy ( - Célula 5: nlp = spacy.load("en_core_web_sm"))
nlp = spacy.load("en_core_web_sm")

# Corpus base para o vectorizer 
corpus = [
    "cloud computing is scalable",
    "AI is transforming cloud services"
]

# Função da biblioteca Scikit Learn para vetorização de texto 
vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)


def process_pipeline(text: str) -> dict:
    """
    Pipeline de NLP com as técnicas ensinadas na .
    Segue a mesma sequência do notebook .
    """

    # --- Morphologia ---

    # Exemplo de uso da técnica stemming 
    stemmer = PorterStemmer()

    # Exemplo de uso da técnica Lematização 
    lemmatizer = WordNetLemmatizer()

    # Tokenização com NLTK 
    tokens = word_tokenize(text)

    # Stemming de cada token
    stems = [stemmer.stem(t) for t in tokens]

    # Lematização de cada token
    lemmas = [lemmatizer.lemmatize(t) for t in tokens]

    # --- Sintaxe ---

    # Exemplo de uso da técnica de análise sintática Part-Of-Speech 
    doc = nlp(text)
    pos_tags = [
        {"token": token.text, "pos": token.pos_, "dep": token.dep_, "head": token.head.text}
        for token in doc
    ]

    # Exemplo de uso da técnica de tokenização com spaCy 
    tokens_spacy = [token.text for token in doc]

    # --- Vetorização ---

    # Função da biblioteca Scikit Learn para vetorização de texto 
    X = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    vector = dict(zip(feature_names, [round(v, 4) for v in X.toarray()[0]]))

    # --- Sentimento ---

    # Análise de sentimento léxica 
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
            "subjetividade": round(subjectivity, 4)
        }
    }


if __name__ == "__main__":
    resultado = process_pipeline("The new API is amazing")
    import json
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
