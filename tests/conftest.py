import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

# Banco SQLite em memória, isolado da base usada em desenvolvimento/produção.
# StaticPool garante que todas as conexões (inclusive as abertas pela
# BackgroundTask) reutilizem a MESMA conexão, já que ":memory:" cria um
# banco novo e vazio a cada conexão nova por padrão.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session, monkeypatch):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # A importação de CSV roda em BackgroundTasks e abre sua PRÓPRIA sessão
    # via SessionLocal (não passa pela dependency_overrides). Precisamos
    # redirecionar essa SessionLocal para o banco de testes também, senão
    # o teste grava no job_board.db real.
    import app.routers.vagas as vagas_module
    monkeypatch.setattr(vagas_module, "SessionLocal", TestingSessionLocal)

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
