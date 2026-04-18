# 221332 - Projetar Aplicacoes Baseadas em IA na Nuvem

## Fase 2

Este repositorio contem a evolucao da API da fase 1 para atender os requisitos da fase 2:

- API REST documentada com FastAPI
- autenticacao por chave de API
- containerizacao com Docker
- pipeline de CI com GitHub Actions
- deploy manual para Heroku usando imagem publicada no Docker Hub

## Integrantes

- Alysson Leandro Nascimento de Oliveira
- Edcarla Sousa de Jesus
- Nereu Necholson Vieira de Lacerda Junior

## Estrutura

- `api.py`: aplicacao FastAPI e rotas
- `preprocessing.py`: pipeline de NLP
- `dataset_tmdb_completo.csv`: base usada pela API
- `221332_PROJETAR_APLICACOES_BASEADAS_EM_IA_NA_NUVEM.ipynb`: notebook da entrega
- `Dockerfile`: imagem da aplicacao
- `.github/workflows/ci.yml`: build e testes
- `.github/workflows/deploy-heroku.yml`: publicacao no Docker Hub e deploy manual no Heroku

## Requisitos

- Python 3.11+
- Docker

Instalacao local:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python api.py
```

## Variaveis de ambiente

- `API_KEY`: chave usada nas rotas protegidas
- `PORT`: porta da aplicacao
- `DATASET_PATH`: caminho alternativo para o dataset

Se `API_KEY` nao for definida, a aplicacao usa `dev-api-key` para facilitar testes locais.

## Execucao local

```bash
$env:API_KEY="minha-chave"
python api.py
```

Documentacao Swagger:

- `http://localhost:8000/docs`

## Executando com Docker

Build:

```bash
docker build -t 221332-fase2-api .
```

Run:

```bash
docker run -p 8000:8000 -e PORT=8000 -e API_KEY=minha-chave 221332-fase2-api
```

## Endpoints

Publicos:

- `GET /`
- `GET /health`

Protegidos com header `X-API-Key`:

- `GET /filme-aleatorio`
- `POST /analisar`

Exemplo de chamada:

```bash
curl -X POST "http://localhost:8000/analisar" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: minha-chave" ^
  -d "{\"texto\":\"The movie was amazing\"}"
```

## GitHub Actions

### CI

O workflow `ci.yml`:

- instala as dependencias
- baixa os recursos de NLP
- valida os arquivos Python
- roda os testes
- monta a imagem Docker

### Deploy manual

O workflow `deploy-heroku.yml`:

- publica a imagem `latest` no Docker Hub
- configura a stack `container` no Heroku
- envia a imagem para `registry.heroku.com`
- faz o release manual via `workflow_dispatch`

## GitHub Secrets necessarios

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `HEROKU_API_KEY`
- `HEROKU_EMAIL`
- `HEROKU_APP_NAME`
- `APP_API_KEY`

## Observacao sobre a imagem

O workflow publica apenas a tag `latest`, o que ajuda a manter uma unica imagem ativa no fluxo do projeto.
