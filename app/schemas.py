# app/schemas.py
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

# ==========================================
# SCHEMAS DE EMPRESA
# ==========================================


class EmpresaCreate(BaseModel):
    nome: str = Field(..., min_length=1, max_length=200)
    setor: str = Field(..., min_length=1, max_length=100)


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    setor: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SCHEMAS DE VAGA
# ==========================================


class VagaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descricao: str = Field(..., min_length=1)
    senioridade: str = Field(..., min_length=1, max_length=50)  # Junior, Pleno, Senior
    empresa_id: int


class VagaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    senioridade: str
    empresa_id: int
    empresa: Optional[EmpresaResponse] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# SCHEMAS DE IMPORTAÇÃO CSV
# ==========================================


class ImportacaoCSVResponse(BaseModel):
    id: int
    arquivo: str
    status: str
    total_linhas: int
    linhas_sucesso: int
    linhas_falha: int
    erros: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
