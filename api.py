from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os

from preprocessing import process_pipeline

# Criação da aplicação FastAPI 
app = FastAPI(
    title="221332 - API de Análise de Sentimento",
    description="API REST para análise de sentimento de sinopses de filmes. Pipeline NLP conforme .",
    version="1.0.0"
)

# CORS — permite requisições do Next.js (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de dados com Pydantic 
class SinopseInput(BaseModel):
    texto: str


DATASET_PATH = "dataset_tmdb_completo.csv"


# Endpoint GET 
@app.get("/")
def status():
    """Retorna o status da API e total de filmes no dataset."""
    info = {"status": "online", "descricao": "API 221332 - Fase 1"}
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_csv(DATASET_PATH)
            info["total_filmes"] = len(df)
        except Exception:
            pass
    return info


# Endpoint GET — filme aleatório para o sorteiro do frontend
@app.get("/filme-aleatorio")
def filme_aleatorio():
    """Retorna um filme aleatório do dataset com sinopse em PT e EN."""
    if not os.path.exists(DATASET_PATH):
        raise HTTPException(status_code=404, detail="Dataset não encontrado.")
    try:
        df = pd.read_csv(DATASET_PATH)
        enriched = df[df['overview_en'].notna() & (df['overview_en'] != "")]
        if enriched.empty:
            raise HTTPException(status_code=404, detail="Nenhum filme enriquecido disponível.")
        row = enriched.sample(1).iloc[0]
        return {
            "title": row.get("title", ""),
            "overview": row.get("overview", ""),
            "overview_en": row.get("overview_en", ""),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint POST 
@app.post("/analisar")
def analisar_sinopse(sinopse: SinopseInput):
    """
    Executa o pipeline de NLP completo  sobre a sinopse fornecida.
    Retorna tokens, stems, lemas, POS tags, vetor TF-IDF e sentimento.
    """
    if not sinopse.texto.strip():
        raise HTTPException(status_code=400, detail="O campo 'texto' não pode estar vazio.")

    try:
        resultado = process_pipeline(sinopse.texto)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
