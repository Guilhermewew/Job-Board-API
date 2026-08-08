# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    setor = Column(String, nullable=False)

    # Relacionamento: 1 empresa tem várias vagas
    vagas = relationship("Vaga", back_populates="empresa", cascade="all, delete-orphan")


class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    senioridade = Column(String, nullable=False)  # Junior, Pleno, Senior
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)

    # Relacionamento: Várias vagas pertencem a 1 empresa
    empresa = relationship("Empresa", back_populates="vagas")


class ImportacaoCSV(Base):
    """
    Guarda o resultado de cada importação de CSV em segundo plano,
    para que o usuário consiga consultar depois se deu tudo certo.
    """
    __tablename__ = "importacoes_csv"

    id = Column(Integer, primary_key=True, index=True)
    arquivo = Column(String, nullable=False)
    status = Column(String, default="processando")  # processando | concluido | erro
    total_linhas = Column(Integer, default=0)
    linhas_sucesso = Column(Integer, default=0)
    linhas_falha = Column(Integer, default=0)
    erros = Column(String, nullable=True)  # texto com detalhes das linhas que falharam
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
