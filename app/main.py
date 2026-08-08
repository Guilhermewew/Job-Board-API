# app/main.py
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import empresas, vagas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Board API",
    description="API para gerenciamento de vagas de emprego e empresas.",
    version="0.1.0"
)

app.include_router(empresas.router)
app.include_router(vagas.router)


@app.get("/")
def read_root():
    return {"mensagem": "API de Vagas rodando com sucesso! Acesse /docs para testar."}
