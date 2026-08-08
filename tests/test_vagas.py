import io


def _criar_empresa(client, nome="Acme Corp"):
    return client.post("/empresas/", json={"nome": nome, "setor": "Tecnologia"}).json()


def test_criar_vaga_sucesso(client):
    empresa = _criar_empresa(client)

    response = client.post("/vagas/", json={
        "titulo": "Desenvolvedor Backend Jr",
        "descricao": "Vaga para atuar com FastAPI",
        "senioridade": "Junior",
        "empresa_id": empresa["id"],
    })

    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Desenvolvedor Backend Jr"
    assert data["empresa"]["nome"] == "Acme Corp"


def test_criar_vaga_com_empresa_inexistente_retorna_404(client):
    response = client.post("/vagas/", json={
        "titulo": "Desenvolvedor Backend Jr",
        "descricao": "Vaga para atuar com FastAPI",
        "senioridade": "Junior",
        "empresa_id": 9999,
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Empresa não encontrada."


def test_criar_vaga_campo_faltando_retorna_422(client):
    response = client.post("/vagas/", json={"titulo": "Sem descrição"})
    assert response.status_code == 422


def test_listar_vagas_vazio(client):
    response = client.get("/vagas/")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_vagas_filtro_senioridade(client):
    empresa = _criar_empresa(client)
    client.post("/vagas/", json={
        "titulo": "Dev Jr", "descricao": "x", "senioridade": "Junior", "empresa_id": empresa["id"]
    })
    client.post("/vagas/", json={
        "titulo": "Dev Sr", "descricao": "x", "senioridade": "Senior", "empresa_id": empresa["id"]
    })

    response = client.get("/vagas/?senioridade=Senior")
    assert response.status_code == 200
    resultados = response.json()
    assert len(resultados) == 1
    assert resultados[0]["titulo"] == "Dev Sr"


def test_obter_vaga_inexistente_retorna_404(client):
    response = client.get("/vagas/999")
    assert response.status_code == 404


def test_importar_csv_arquivo_valido(client):
    empresa = _criar_empresa(client)
    csv_conteudo = (
        "titulo,descricao,senioridade,empresa_id\n"
        f"Dev Pleno,Vaga via CSV,Pleno,{empresa['id']}\n"
        f"Dev Senior,Outra vaga via CSV,Senior,{empresa['id']}\n"
    )
    arquivo = io.BytesIO(csv_conteudo.encode("utf-8"))

    response = client.post(
        "/vagas/importar-csv/",
        files={"arquivo": ("vagas.csv", arquivo, "text/csv")},
    )
    assert response.status_code == 202
    importacao_id = response.json()["id"]

    # TestClient roda BackgroundTasks de forma síncrona antes de devolver a resposta,
    # então já podemos consultar o status e a listagem de vagas em seguida.
    status = client.get(f"/vagas/importar-csv/{importacao_id}").json()
    assert status["status"] == "concluido"
    assert status["linhas_sucesso"] == 2
    assert status["linhas_falha"] == 0

    vagas = client.get("/vagas/").json()
    assert len(vagas) == 2


def test_importar_csv_com_linha_invalida_nao_derruba_as_validas(client):
    """
    Este é o teste que expõe o bug original: antes, uma linha com empresa_id
    inválido abortava o import inteiro e NENHUMA vaga era salva, mesmo as
    linhas corretas. Agora as válidas devem ser salvas e a inválida reportada.
    """
    empresa = _criar_empresa(client)
    csv_conteudo = (
        "titulo,descricao,senioridade,empresa_id\n"
        f"Dev Pleno,Vaga valida,Pleno,{empresa['id']}\n"
        "Dev Quebrado,Vaga invalida,Senior,nao-e-um-numero\n"
    )
    arquivo = io.BytesIO(csv_conteudo.encode("utf-8"))

    response = client.post(
        "/vagas/importar-csv/",
        files={"arquivo": ("vagas.csv", arquivo, "text/csv")},
    )
    importacao_id = response.json()["id"]

    status = client.get(f"/vagas/importar-csv/{importacao_id}").json()
    assert status["status"] == "concluido"
    assert status["linhas_sucesso"] == 1
    assert status["linhas_falha"] == 1
    assert status["erros"] is not None

    vagas = client.get("/vagas/").json()
    assert len(vagas) == 1
    assert vagas[0]["titulo"] == "Dev Pleno"


def test_importar_csv_extensao_invalida_retorna_422(client):
    arquivo = io.BytesIO(b"conteudo qualquer")
    response = client.post(
        "/vagas/importar-csv/",
        files={"arquivo": ("vagas.txt", arquivo, "text/plain")},
    )
    assert response.status_code == 422
