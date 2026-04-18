# 221332 - Projetar Aplicacoes Baseadas em IA na Nuvem

## Fase 2 - API de Analise de Sentimento

API REST para analise de sentimento de sinopses de filmes com pipeline de NLP, autenticacao por chave de API, containerizacao com Docker, publicacao no Docker Hub e deploy publico no Render.

## Caracteristicas principais

- API REST desenvolvida com FastAPI
- Documentacao automatica com Swagger e OpenAPI
- Autenticacao por `X-API-Key`
- Pipeline NLP com tokenizacao, stemming, lemmatizacao, POS tags, TF-IDF e analise de sentimento
- Container Docker para execucao em ambiente padronizado
- CI com GitHub Actions para testes e build
- Deploy manual no Render via GitHub Actions e Deploy Hook

## Links do projeto

- Repositorio GitHub: [https://github.com/nereuvjr-br/221332-Fase2](https://github.com/nereuvjr-br/221332-Fase2)
- API publica: [https://two21332-fase2.onrender.com](https://two21332-fase2.onrender.com)
- Swagger: [https://two21332-fase2.onrender.com/docs](https://two21332-fase2.onrender.com/docs)
- Healthcheck: [https://two21332-fase2.onrender.com/health](https://two21332-fase2.onrender.com/health)
- Docker Hub: [https://hub.docker.com/r/nereuvljr/221332-fase1](https://hub.docker.com/r/nereuvljr/221332-fase1)

## Integrantes

- Alysson Leandro Nascimento de Oliveira
- Edcarla Sousa de Jesus
- Nereu Necholson Vieira de Lacerda Junior

## Estrutura do projeto

```text
.
├── api.py
├── preprocessing.py
├── dataset_tmdb_completo.csv
├── requirements.txt
├── Dockerfile
├── 221332_PROJETAR_APLICACOES_BASEADAS_EM_IA_NA_NUVEM.ipynb
├── README.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy-render.yml
└── tests/
    └── test_api.py
```

## Requisitos

- Python 3.11+
- pip
- Docker

## Dependencias principais

- `fastapi`
- `uvicorn`
- `spacy`
- `nltk`
- `textblob`
- `scikit-learn`
- `pandas`

## Inicio rapido

### 1. Clonar o repositorio

```bash
git clone https://github.com/nereuvjr-br/221332-Fase2.git
cd 221332-Fase2
```

### 2. Instalar dependencias

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Instalacao:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Executar localmente

PowerShell:

```bash
$env:API_KEY="dd9cb1d3ffb566082432d8d1077ca2f8"
$env:PORT="8000"
python api.py
```

CMD:

```bash
set API_KEY=dd9cb1d3ffb566082432d8d1077ca2f8
set PORT=8000
python api.py
```

Linux/macOS:

```bash
export API_KEY="dd9cb1d3ffb566082432d8d1077ca2f8"
export PORT="8000"
python api.py
```

Documentacao local:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Execucao com Docker

### Build da imagem

```bash
docker build -t nereuvljr/221332-fase1:latest .
```

### Execucao do container

```bash
docker run -p 8000:8000 -e PORT=8000 -e API_KEY=dd9cb1d3ffb566082432d8d1077ca2f8 nereuvljr/221332-fase1:latest
```

## Endpoints

### Publicos

| Metodo | Endpoint | Descricao |
|---|---|---|
| `GET` | `/` | Status geral da API |
| `GET` | `/health` | Healthcheck da aplicacao |

### Protegidos

Enviar o header:

```text
X-API-Key: dd9cb1d3ffb566082432d8d1077ca2f8
```

| Metodo | Endpoint | Descricao |
|---|---|---|
| `GET` | `/filme-aleatorio` | Retorna um filme aleatorio do dataset |
| `POST` | `/analisar` | Analisa o texto recebido |

## Exemplos de uso

### Status da API

```bash
curl https://two21332-fase2.onrender.com/
```

Resposta esperada:

```json
{
  "status": "online",
  "descricao": "API 221332 - Fase 2",
  "docs": "/docs",
  "healthcheck": "/health",
  "seguranca": "Envie o cabecalho X-API-Key nas rotas protegidas.",
  "total_filmes": 2000
}
```

### Healthcheck

```bash
curl https://two21332-fase2.onrender.com/health
```

### Obter filme aleatorio

```bash
curl -X GET "https://two21332-fase2.onrender.com/filme-aleatorio" ^
  -H "X-API-Key: dd9cb1d3ffb566082432d8d1077ca2f8"
```

### Analisar sentimento

```bash
curl -X POST "https://two21332-fase2.onrender.com/analisar" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: dd9cb1d3ffb566082432d8d1077ca2f8" ^
  -d "{\"texto\":\"The movie was amazing\"}"
```

Resposta resumida:

```json
{
  "texto_original": "The movie was amazing",
  "tokens_nltk": ["The", "movie", "was", "amazing"],
  "stems": ["the", "movi", "wa", "amaz"],
  "lemmas": ["The", "movie", "wa", "amazing"],
  "tokens_spacy": ["The", "movie", "was", "amazing"],
  "sentimento": {
    "classificacao": "Positivo",
    "polaridade": 0.6,
    "subjetividade": 0.9
  }
}
```

## Pipeline de NLP

O endpoint `POST /analisar` executa:

| Etapa | Biblioteca | Descricao |
|---|---|---|
| Tokenizacao | NLTK | Divide o texto em tokens |
| Stemming | NLTK | Reduz palavras a raiz |
| Lemmatizacao | NLTK | Normaliza palavras |
| POS Tags | spaCy | Classificacao gramatical |
| Dependencias | spaCy | Relacoes sintaticas entre termos |
| TF-IDF | scikit-learn | Vetorizacao do texto |
| Sentimento | TextBlob | Classificacao, polaridade e subjetividade |

## Variaveis de ambiente

| Variavel | Padrao | Descricao |
|---|---|---|
| `API_KEY` | `dev-api-key` | Chave para endpoints protegidos |
| `PORT` | `8000` | Porta da aplicacao |
| `DATASET_PATH` | `dataset_tmdb_completo.csv` | Caminho do dataset |
| `SPACY_MODEL` | `en_core_web_sm` | Modelo spaCy utilizado |

## Testes

Executar testes:

```bash
pytest tests/ -v
```

Ou:

```bash
python -m pytest -q
```

Testes incluidos:

- `GET /` retorna status corretamente
- `GET /health` retorna `healthy`
- `/analisar` exige autenticacao
- `/analisar` processa o texto com sucesso

## GitHub Actions e CI/CD

### CI

Arquivo: `.github/workflows/ci.yml`

Executado em:

- `push` na branch principal
- `pull_request`

Etapas:

- instalacao das dependencias
- download dos recursos NLP
- validacao dos arquivos Python
- execucao dos testes
- build da imagem Docker

### Deploy manual no Render

Arquivo: `.github/workflows/deploy-render.yml`

Acionado manualmente com `workflow_dispatch`.

Etapas:

- login no Docker Hub
- build da imagem da aplicacao
- publicacao da tag `latest`
- chamada do `Deploy Hook` do Render

## GitHub Secrets necessarios

Configurar em `Settings > Secrets and variables > Actions`:

```text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
RENDER_DEPLOY_HOOK_URL
```

## Deploy no Render

O deploy publico esta disponivel em:

- [https://two21332-fase2.onrender.com](https://two21332-fase2.onrender.com)

Configuracao utilizada:

- tipo de servico: `Web Service`
- imagem: `docker.io/nereuvljr/221332-fase1:latest`
- deploy manual por `Deploy Hook`

## Troubleshooting

### Modelo spaCy nao encontrado

```bash
python -m spacy download en_core_web_sm
```

### API key invalida

Confirme se o header foi enviado corretamente:

```text
X-API-Key: dd9cb1d3ffb566082432d8d1077ca2f8
```

### Dataset nao encontrado

Confirme se o arquivo `dataset_tmdb_completo.csv` esta presente na raiz do projeto ou configure `DATASET_PATH`.

### Erro no Docker

```bash
docker ps
docker logs <container-id>
```

## Arquitetura

```text
Cliente HTTP
   |
   | JSON + X-API-Key
   v
FastAPI (api.py)
   |
   +-- Dataset TMDB
   |
   +-- Pipeline NLP (preprocessing.py)
         |
         +-- spaCy
         +-- NLTK
         +-- TextBlob
         +-- scikit-learn
```

## Observacoes para avaliacao

- O projeto possui API publica em producao
- A documentacao interativa esta disponivel em `/docs`
- A imagem Docker foi publicada no Docker Hub
- O repositorio possui pipeline de CI e deploy manual
- A chave de acesso foi mantida no README para facilitar a validacao pelo professor

## Licenca

Projeto academico desenvolvido para a disciplina de Projetar Aplicacoes Baseadas em IA na Nuvem.
