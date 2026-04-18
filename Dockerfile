FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm \
    && python - <<'PY'
import nltk
for package in ("wordnet", "omw-1.4", "punkt", "punkt_tab"):
    nltk.download(package, quiet=True)
PY

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
