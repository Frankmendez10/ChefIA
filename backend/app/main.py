from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.assistant import router as assistant_router


app = FastAPI(
    title="ChefIA API",
    description="API para el asistente culinario inteligente ChefIA",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistant_router)


@app.get("/")
def root():
    return {
        "message": "ChefIA API funcionando",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }