# 221332 - PROJETAR APLICAÇÕES BASEADAS EM IA NA NUVEM

## Projeto Fase 1 — Entrega Final

Este repositório contém a implementação da **Fase 1** do projeto da disciplina de Projetar Aplicações Baseadas em IA na Nuvem. O objetivo principal é o desenvolvimento de uma API REST funcional, estruturada para o processamento de Processamento de Linguagem Natural (NLP) e preparada para integração com modelos de análise de sentimento.

---

### Instituição:
*   **Faculdade**: UNIFACISA
*   **Curso**: Inteligência Artificial
*   **Professor**: Matheus Batista Silva

### Equipe:
*   Alysson Leandro Nascimento de Oliveira
*   Edcarla Sousa de Jesus
*   Nereu Necholson Vieira de Lacerda Júnior

---

## 🚀 Tecnologias Utilizadas

A aplicação foi desenvolvida utilizando as seguintes bibliotecas e frameworks:

*   **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e de alta performance para construção de APIs com Python.
*   **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para execução da API.
*   **[NLTK](https://www.nltk.org/)**: Ferramentas para tokenização, stemming (Porter) e lemmatization (WordNet).
*   **[spaCy](https://spacy.io/)**: Processamento industrial de NLP, utilizado para análise sintática (POS Tagging).
*   **[TextBlob](https://textblob.readthedocs.io/en/dev/)**: Processamento de dados textuais para análise inicial de polaridade e subjetividade (Léxico).
*   **[Scikit-Learn](https://scikit-learn.org/)**: Utilizado para a etapa de vetorização (TF-IDF).
*   **[Pandas](https://pandas.pydata.org/)**: Manipulação do dataset TMDB para extração de sinopses.

---

## 📋 Requisitos da Fase 1

Conforme as diretrizes do projeto, foram implementados:

1.  **API REST Funcional**: Desenvolvida em Python com FastAPI.
2.  **Preparação para Análise de Sentimento**: Integração de um pipeline completo de NLP que prepara o dado bruto para classificação.
3.  **Método GET**: Implementado para verificação de status e fornecimento de dados aleatórios.
4.  **Método POST**: Implementado para processamento e análise técnica de uma sinopse fornecida pelo usuário.

---

## 🛠️ Como Executar o Projeto

1.  **Clone o repositório**:
    ```bash
    git clone [URL_DO_REPOSITORIO]
    cd [NOME_DA_PASTA]
    ```

2.  **Instale as dependências**:
    ```bash
    pip install fastapi uvicorn spacy nltk textblob scikit-learn pandas
    ```

3.  **Baixe os modelos necessários**:
    ```bash
    python -m spacy download en_core_web_sm
    ```

4.  **Inicie a API**:
    ```bash
    python api.py
    ```
    A API estará disponível em `http://localhost:8000`. A documentação interativa (Swagger) pode ser acessada em `http://localhost:8000/docs`.

---

## 📡 Endpoints da API

### `GET /`
Verifica a disponibilidade da API e retorna informações básicas sobre o dataset.
*   **Resposta**: JSON com status e total de filmes disponíveis.

### `GET /filme-aleatorio`
Retorna um filme aleatório do dataset `dataset_tmdb_completo.csv`.
*   **Resposta**: JSON com título, sinopse (PT) e sinopse enriquecida (EN).

### `POST /analisar`
Recebe um texto (sinopse) e executa o pipeline de NLP completo.
*   **Corpo da Requisição**:
    ```json
    {
      "texto": "The movie was an incredible journey through space."
    }
    ```
*   **Processamento Realizado**:
    *   **Morfologia**: Tokenização, Stemming e Lematização.
    *   **Sintaxe**: Part-Of-Speech (POS) Tagging e Dependências Sintáticas.
    *   **Vetorização**: Conversão do texto em vetor TF-IDF.
    *   **Análise Inicial**: Classificação de polaridade (Positivo, Negativo ou Neutro).

---

## 📂 Estrutura do Projeto

*   `api.py`: Ponto de entrada da aplicação FastAPI e definição das rotas.
*   `preprocessing.py`: Lógica central do pipeline de NLP, contendo as funções de processamento.
*   `221332_PROJETAR_APLICACOES_BASEADAS_EM_IA_NA_NUVEM.ipynb`: Notebook de desenvolvimento e experimentação das técnicas de IA. ([Versão Google Colab](https://colab.research.google.com/drive/1qi6sDe4a3t-5CV7Tyig3NWs24s3pM7VP?usp=sharing))
*   `dataset_tmdb_completo.csv`: Dataset base para sugestão de filmes.

---
> Projeto desenvolvido para a disciplina de **Projetar Aplicações Baseadas em IA na Nuvem** - 2026.
