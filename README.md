# 221332 - Projetar Aplicacoes Baseadas em IA na Nuvem

## Fase 2

Este repositorio contem a evolucao da API da fase 1 para atender os requisitos da fase 2:

- API REST documentada com FastAPI
- autenticacao por chave de API
- containerizacao com Docker
- pipeline de CI com GitHub Actions
- publicacao da imagem no Docker Hub
- deploy manual no Render via GitHub Actions

## Links do projeto

- API publica: [https://two21332-fase2.onrender.com](https://two21332-fase2.onrender.com)
- Swagger: [https://two21332-fase2.onrender.com/docs](https://two21332-fase2.onrender.com/docs)
- Healthcheck: [https://two21332-fase2.onrender.com/health](https://two21332-fase2.onrender.com/health)
- Docker Hub: [https://hub.docker.com/r/nereuvljr/221332-fase1](https://hub.docker.com/r/nereuvljr/221332-fase1)

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
- `.github/workflows/deploy-render.yml`: publicacao no Docker Hub e deploy manual no Render

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

Chave configurada para uso atual da API publicada:

```text
API_KEY=dd9cb1d3ffb566082432d8d1077ca2f8
```

Se `API_KEY` nao for definida, a aplicacao usa `dev-api-key` para facilitar testes locais.

## Execucao local

```bash
$env:API_KEY="minha-chave"
python api.py
```

Documentacao Swagger:

- `http://localhost:8000/docs`
- `https://two21332-fase2.onrender.com/docs`

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
  -H "X-API-Key: dd9cb1d3ffb566082432d8d1077ca2f8" ^
  -d "{\"texto\":\"The movie was amazing\"}"
```

Exemplo em producao:

```bash
curl -X POST "https://two21332-fase2.onrender.com/analisar" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: dd9cb1d3ffb566082432d8d1077ca2f8" ^
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

### Deploy manual no Render

O workflow `deploy-render.yml`:

- faz login no Docker Hub
- gera a imagem da aplicacao
- publica apenas a tag `latest`
- aciona manualmente o deploy no Render por meio de um `Deploy Hook`

Esse fluxo atende ao requisito de implantacao manual. O workflow so roda quando alguem clicar em `Run workflow` no GitHub Actions.

## GitHub Secrets necessarios

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `RENDER_DEPLOY_HOOK_URL`

## Como configurar o Render

1. Crie um `Web Service` no Render do tipo `Image-backed service`.
2. Aponte a imagem para:

```text
docker.io/nereuvljr/221332-fase1:latest
```

3. Configure a variavel de ambiente:

```text
API_KEY=dd9cb1d3ffb566082432d8d1077ca2f8
```

4. Copie o `Deploy Hook` em `Settings` no Render.
5. Salve esse valor no GitHub em `Settings > Secrets and variables > Actions` com o nome `RENDER_DEPLOY_HOOK_URL`.

## Observacao sobre a imagem

O workflow publica apenas a tag `latest`, o que ajuda a manter uma unica imagem ativa no fluxo pedido pelo projeto.

## Observacao sobre a pipeline

O arquivo `.github/workflows/ci.yml` cobre o build da aplicacao.

O arquivo `.github/workflows/deploy-render.yml` cobre a publicacao da imagem e o deploy manual no Render.
