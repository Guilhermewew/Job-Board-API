def test_criar_empresa_sucesso(client):
    response = client.post("/empresas/", json={"nome": "Acme Corp", "setor": "Tecnologia"})
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Acme Corp"
    assert data["setor"] == "Tecnologia"
    assert "id" in data


def test_criar_empresa_sem_nome_retorna_422(client):
    response = client.post("/empresas/", json={"setor": "Tecnologia"})
    assert response.status_code == 422


def test_criar_empresa_nome_vazio_retorna_422(client):
    response = client.post("/empresas/", json={"nome": "", "setor": "Tecnologia"})
    assert response.status_code == 422


def test_listar_empresas_vazio(client):
    response = client.get("/empresas/")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_empresas_apos_criar(client):
    client.post("/empresas/", json={"nome": "Acme Corp", "setor": "Tecnologia"})
    client.post("/empresas/", json={"nome": "Beta Ltda", "setor": "Varejo"})

    response = client.get("/empresas/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_obter_empresa_existente(client):
    criada = client.post("/empresas/", json={"nome": "Acme Corp", "setor": "Tecnologia"}).json()

    response = client.get(f"/empresas/{criada['id']}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Acme Corp"


def test_obter_empresa_inexistente_retorna_404(client):
    response = client.get("/empresas/999")
    assert response.status_code == 404
