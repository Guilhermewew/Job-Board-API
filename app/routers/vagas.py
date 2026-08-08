# app/routers/vagas.py
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas
from ..database import get_db, SessionLocal

router = APIRouter(
    prefix="/vagas",
    tags=["Vagas"]
)

CAMPOS_OBRIGATORIOS = ("titulo", "descricao", "senioridade", "empresa_id")


# ==========================================
# FUNÇÃO DE SEGUNDO PLANO (O "ROBÔ")
# ==========================================
def processar_vagas_csv(conteudo_csv: str, importacao_id: int):
    """
    Roda em segundo plano. Processa o CSV linha por linha; uma linha inválida
    NÃO derruba as demais (antes, um erro em qualquer linha abortava o
    import inteiro sem salvar nada e sem avisar o usuário).
    """
    db = SessionLocal()
    importacao = db.query(models.ImportacaoCSV).filter(
        models.ImportacaoCSV.id == importacao_id
    ).first()

    try:
        arquivo_em_memoria = io.StringIO(conteudo_csv)
        leitor = csv.DictReader(arquivo_em_memoria)

        total = 0
        sucesso = 0
        erros = []

        for numero_linha, linha in enumerate(leitor, start=2):  # linha 1 = cabeçalho
            total += 1

            faltando = [c for c in CAMPOS_OBRIGATORIOS if not linha.get(c)]
            if faltando:
                erros.append(f"Linha {numero_linha}: campos ausentes {faltando}")
                continue

            try:
                empresa_id = int(linha["empresa_id"])
            except (ValueError, TypeError):
                erros.append(f"Linha {numero_linha}: empresa_id inválido ('{linha.get('empresa_id')}')")
                continue

            empresa_existe = db.query(models.Empresa.id).filter(
                models.Empresa.id == empresa_id
            ).first()
            if not empresa_existe:
                erros.append(f"Linha {numero_linha}: empresa_id {empresa_id} não existe")
                continue

            nova_vaga = models.Vaga(
                titulo=linha["titulo"],
                descricao=linha["descricao"],
                senioridade=linha["senioridade"],
                empresa_id=empresa_id,
            )
            db.add(nova_vaga)
            sucesso += 1

        db.commit()  # salva todas as vagas válidas, mesmo que outras tenham falhado

        if importacao:
            importacao.status = "concluido"
            importacao.total_linhas = total
            importacao.linhas_sucesso = sucesso
            importacao.linhas_falha = total - sucesso
            importacao.erros = "; ".join(erros) if erros else None
            db.commit()

    except Exception as e:
        db.rollback()
        if importacao:
            importacao.status = "erro"
            importacao.erros = str(e)
            db.commit()
    finally:
        db.close()


# ==========================================
# ROTAS NORMAIS DA API
# ==========================================

@router.post("/importar-csv/", response_model=schemas.ImportacaoCSVResponse, status_code=202)
async def importar_vagas_csv(
    background_tasks: BackgroundTasks,
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not arquivo.filename.endswith(".csv"):
        raise HTTPException(status_code=422, detail="O arquivo precisa ser .csv")

    conteudo_bytes = await arquivo.read()
    conteudo_str = conteudo_bytes.decode("utf-8")

    # Cria o registro de status ANTES de disparar a tarefa, para já devolver um id
    importacao = models.ImportacaoCSV(arquivo=arquivo.filename, status="processando")
    db.add(importacao)
    db.commit()
    db.refresh(importacao)

    background_tasks.add_task(processar_vagas_csv, conteudo_str, importacao.id)

    return importacao


@router.get("/importar-csv/{importacao_id}", response_model=schemas.ImportacaoCSVResponse)
def status_importacao(importacao_id: int, db: Session = Depends(get_db)):
    importacao = db.query(models.ImportacaoCSV).filter(
        models.ImportacaoCSV.id == importacao_id
    ).first()
    if not importacao:
        raise HTTPException(status_code=404, detail="Importação não encontrada.")
    return importacao


@router.post("/", response_model=schemas.VagaResponse, status_code=201)
def criar_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db)):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == vaga.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")

    db_vaga = models.Vaga(**vaga.model_dump())
    db.add(db_vaga)
    db.commit()
    db.refresh(db_vaga)
    return db_vaga


@router.get("/", response_model=List[schemas.VagaResponse])
def listar_vagas(senioridade: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Vaga)
    if senioridade:
        query = query.filter(models.Vaga.senioridade == senioridade)
    return query.all()


@router.get("/{vaga_id}", response_model=schemas.VagaResponse)
def obter_vaga(vaga_id: int, db: Session = Depends(get_db)):
    vaga = db.query(models.Vaga).filter(models.Vaga.id == vaga_id).first()
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada.")
    return vaga
