# ChefIA

Asistente culinario inteligente desarrollado como proyecto final del hackathon.

ChefIA permite consultar recetas, sustituciones de ingredientes, información culinaria y recomendaciones mediante una arquitectura que combina clasificación de intención, recuperación de información (RAG) y un modelo de lenguaje ajustado con LoRA.

## Características

* Clasificación de consultas en cuatro intenciones:

  * `RECIPE`
  * `SUBSTITUTION`
  * `QUESTION`
  * `RECOMMENDATION`
* Recuperación de información mediante RAG.
* Búsqueda semántica con embeddings y FAISS.
* Modelo TinyLlama-1.1B-Chat-v1.0.
* Fine-tuning mediante LoRA.
* Respuestas basadas en información disponible en la base de conocimiento.
* API REST con FastAPI.
* Interfaz web con React y TypeScript.
* Tests unitarios y pruebas end-to-end.

## Arquitectura

```text
Usuario
   │
   ▼
React + TypeScript
   │
   │ HTTP POST
   ▼
FastAPI
   │
   ▼
Clasificación de intención
   │
   ├───────────────┐
   │               │
   ▼               ▼
RAG             TinyLlama
Retriever       + LoRA
   │               │
   └───────┬───────┘
           ▼
      Respuesta
           │
           ▼
        React
```

## Tecnologías

### Frontend

* React
* TypeScript
* Vite

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### Inteligencia artificial

* TinyLlama 1.1B Chat
* Hugging Face Transformers
* PEFT
* TRL
* PyTorch
* Sentence Transformers
* FAISS

### Datos

* JSON
* Embeddings semánticos
* Base de conocimiento local

### Testing

* Pytest
* Requests

## Estructura del proyecto

```text
ChefIA/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── assistant.py
│   │   ├── rag/
│   │   │   └── retriever.py
│   │   ├── schemas/
│   │   │   └── assistant.py
│   │   ├── services/
│   │   │   ├── assistant_service.py
│   │   │   └── llm_service.py
│   │   └── main.py
│   └── requirements.txt
│
├── ai/
│   ├── dataset/
│   ├── fine_tuning/
│   └── evaluation/
│
├── data/
│   ├── recipes/
│   │   └── recipes.json
│   └── knowledge/
│       ├── ingredients.json
│       ├── substitutions.json
│       └── cooking_knowledge.json
│
├── tests/
│   ├── unit/
│   └── e2e/
│
└── README.md
```

## Flujo de una consulta

Por ejemplo:

```text
"Quiero una cena rápida y saludable"
```

1. ChefIA recibe la consulta desde React.
2. FastAPI recibe la petición.
3. Se clasifica la intención como `RECOMMENDATION`.
4. El Retriever busca recetas relevantes.
5. Se obtiene información de la base de recetas.
6. TinyLlama con LoRA genera una respuesta.
7. El backend estructura la respuesta.
8. React muestra el resultado al usuario.

## RAG

ChefIA utiliza Retrieval-Augmented Generation para proporcionar información relevante al modelo.

El Retriever utiliza:

```text
Sentence Transformers
        ↓
Embeddings
        ↓
FAISS
        ↓
Documentos relevantes
```

La información se obtiene de archivos JSON que contienen:

* recetas
* ingredientes
* sustituciones
* conocimiento culinario

Para deter
