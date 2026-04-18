import os
import secrets
from typing import Annotated

import pandas as pd
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

from preprocessing import process_pipeline

DATASET_PATH = os.getenv("DATASET_PATH", "dataset_tmdb_completo.csv")
API_KEY_NAME = "X-API-Key"
DEFAULT_API_KEY = "dev-api-key"

app = FastAPI(
    title="221332 - API de Analise de Sentimento",
    description=(
        "API REST para analise de sentimento de sinopses de filmes com "
        "documentacao interativa, autenticacao por chave de API e deploy via Docker."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


class SinopseInput(BaseModel):
    texto: str = Field(..., min_length=1, description="Texto a ser analisado.")


def get_expected_api_key() -> str:
    return os.getenv("API_KEY", DEFAULT_API_KEY)


def require_api_key(
    api_key: Annotated[str | None, Security(api_key_header)],
) -> str:
    expected_api_key = get_expected_api_key()
    if not api_key or not secrets.compare_digest(api_key, expected_api_key):
        raise HTTPException(status_code=401, detail="API key invalida ou ausente.")
    return api_key


@app.get("/", tags=["publico"])
def status():
    """Retorna o status da API e total de filmes no dataset."""
    info = {
        "status": "online",
        "descricao": "API 221332 - Fase 2",
        "docs": "/docs",
        "healthcheck": "/health",
        "seguranca": f"Envie o cabecalho {API_KEY_NAME} nas rotas protegidas.",
    }
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_csv(DATASET_PATH)
            info["total_filmes"] = len(df)
        except Exception:
            info["total_filmes"] = "indisponivel"
    return info


@app.get("/health", tags=["publico"])
def health():
    """Healthcheck simples para CI/CD e deploy."""
    return {"status": "healthy"}


@app.get("/filme-aleatorio", tags=["protegido"])
def filme_aleatorio(_: Annotated[str, Security(require_api_key)]):
    """Retorna um filme aleatorio do dataset com sinopse em PT e EN."""
    if not os.path.exists(DATASET_PATH):
        raise HTTPException(status_code=404, detail="Dataset nao encontrado.")

    try:
        df = pd.read_csv(DATASET_PATH)
        enriched = df[df["overview_en"].notna() & (df["overview_en"] != "")]
        if enriched.empty:
            raise HTTPException(
                status_code=404,
                detail="Nenhum filme enriquecido disponivel.",
            )
        row = enriched.sample(1).iloc[0]
        return {
            "title": row.get("title", ""),
            "overview": row.get("overview", ""),
            "overview_en": row.get("overview_en", ""),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/analisar", tags=["protegido"])
def analisar_sinopse(
    sinopse: SinopseInput,
    _: Annotated[str, Security(require_api_key)],
):
    """
    Executa o pipeline de NLP completo sobre a sinopse fornecida.
    Retorna tokens, stems, lemas, POS tags, vetor TF-IDF e sentimento.
    """
    if not sinopse.texto.strip():
        raise HTTPException(status_code=400, detail="O campo 'texto' nao pode estar vazio.")

    try:
        return process_pipeline(sinopse.texto)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no processamento: {exc}",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
