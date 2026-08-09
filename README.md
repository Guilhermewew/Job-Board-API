# Job Board API

API REST para gerenciamento de vagas de emprego e empresas, construída com FastAPI, SQLAlchemy 2.0 e Pydantic v2.

**🔗 API ao vivo:** https://job-board-api-4pdc.onrender.com
**📖 Documentação interativa (Swagger):** https://job-board-api-4pdc.onrender.com/docs

> Nota: o plano gratuito do Render "dorme" a API após um período de inatividade. Se o primeiro acesso demorar ~30-50s pra responder, é isso — é só esperar o servidor acordar.

---

## O problema que este projeto resolve

Empresas de RH e recrutadores costumam receber vagas em planilhas soltas, sem um lugar central pra consultar. Esta API oferece um cadastro estruturado de empresas e vagas, com **importação em lote via CSV** — o fluxo real que muitas empresas usam pra carregar dados históricos — processada em segundo plano pra não travar a requisição em arquivos grandes.

---

## Funcionalidades

| Recurso | Método | Endpoint | Descrição |
|---|---|---|---|
| Empresas | `POST` | `/empresas/` | Cadastra uma nova empresa |
| Empresas | `GET` | `/empresas/` | Lista empresas (com paginação `skip`/`limit`) |
| Empresas | `GET` | `/empresas/{empresa_id}` | Consulta uma empresa pelo ID |
| Vagas | `POST` | `/vagas/` | Cadastra uma nova vaga |
| Vagas | `GET` | `/vagas/` | Lista vagas (filtro opcional `?senioridade=`) |
| Vagas | `GET` | `/vagas/{vaga_id}` | Consulta uma vaga pelo ID |
| Importação | `POST` | `/vagas/importar-csv/` | Importa vagas em lote via CSV (processamento em background) |
| Importação | `GET` | `/vagas/importar-csv/{importacao_id}` | Consulta o status/resultado de uma importação |

---

## Tecnologias

- **Python 3.12** + **FastAPI** (async, validação automática via Pydantic, docs OpenAPI geradas sozinhas)
- **SQLAlchemy 2.0** como ORM
- **Pydantic v2** para schemas de entrada/saída (`EmpresaCreate`/`EmpresaResponse`, `VagaCreate`/`VagaResponse`)
- **PostgreSQL** em produção, **SQLite** automático em desenvolvimento local (sem precisar configurar nada)
- **Docker + docker-compose** para rodar API e banco juntos localmente, espelhando produção
- **pytest** — 16 testes automatizados cobrindo rotas de sucesso, erros (404/422) e o fluxo de importação CSV
- Deploy contínuo no **Render**

---

## Como rodar localmente

### Opção 1 — com Docker (recomendado, já sobe com Postgres)

```bash
git clone https://github.com/Guilhermewew/job_board_api.git
cd job_board_api
docker compose up
```

Acesse: http://localhost:8000/docs

### Opção 2 — direto com Python (usa SQLite, sem dependências externas)

```bash
git clone https://github.com/Guilhermewew/job_board_api.git
cd job_board_api

python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Acesse: http://127.0.0.1:8000/docs

---

## Como rodar os testes

```bash
pytest tests/ -v
```

16 testes, cobrindo: criação e listagem de empresas/vagas, validação de campos (422), busca de recurso inexistente (404), filtro de vagas por senioridade, e importação de CSV — incluindo um teste que reproduz um bug real encontrado durante o desenvolvimento (veja abaixo).

---

## Exemplos de uso

**Cadastrar uma empresa:**

```bash
curl -X POST https://job-board-api-4pdc.onrender.com/empresas/ \
  -H "Content-Type: application/json" \
  -d '{"nome": "TechCorp Brasil", "setor": "Tecnologia"}'
```

**Cadastrar uma vaga:**

```bash
curl -X POST https://job-board-api-4pdc.onrender.com/vagas/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Desenvolvedor Backend Jr", "descricao": "Vaga para atuar com FastAPI", "senioridade": "Junior", "empresa_id": 1}'
```

**Importar vagas por CSV:**

```bash
curl -X POST https://job-board-api-4pdc.onrender.com/vagas/importar-csv/ \
  -F "arquivo=@vagas_exemplo.csv"
```

Formato esperado do CSV (colunas obrigatórias):

```
titulo,descricao,senioridade,empresa_id
Desenvolvedor Python Backend,Vaga remota para atuar com FastAPI,Pleno,1
Analista de Dados Pleno,Atuação com Python e SQL,Pleno,1
```

A resposta do import devolve um `id` de acompanhamento:

```json
{
  "id": 3,
  "arquivo": "vagas_exemplo.csv",
  "status": "processando",
  "total_linhas": 0,
  "linhas_sucesso": 0,
  "linhas_falha": 0,
  "erros": null
}
```

Consulte o resultado com `GET /vagas/importar-csv/{id}` depois de alguns segundos — o status muda para `concluido`, com a contagem de linhas processadas com sucesso e falha, e o detalhe dos erros por linha.

---

## Arquitetura e decisões técnicas

- **FastAPI em vez de Flask/Django:** validação automática via Pydantic, suporte nativo a `async`/`BackgroundTasks` (importante pra importação de arquivos grandes sem travar a requisição) e documentação OpenAPI gerada automaticamente.
- **Schemas separados de entrada e saída** (`*Create` vs `*Response`): evita vazar detalhes internos do banco e permite evoluir o contrato de cada endpoint de forma independente.
- **`DATABASE_URL` via variável de ambiente:** o mesmo código roda com SQLite localmente (zero configuração) e com PostgreSQL em produção, sem precisar trocar uma linha — só define a env var.
- **Importação de CSV em background com rastreamento de status:** cada import cria um registro (`ImportacaoCSV`) que pode ser consultado depois, com contagem de sucesso/falha por linha.

### Bug real encontrado e corrigido

Na primeira versão, o processamento do CSV adicionava cada linha ao banco dentro de um loop, mas só chamava `commit()` **depois** do loop terminar. Isso significava que se **uma única linha** do arquivo tivesse um erro (ex: `empresa_id` inválido), a exceção interrompia o loop antes de chegar no `commit()` — e **nenhuma linha era salva**, nem as que estavam corretas, sem nenhum aviso ao usuário.

A correção trata cada linha individualmente: linhas inválidas são registradas com o motivo do erro e puladas, enquanto as válidas são commitadas normalmente. Esse comportamento está coberto por um teste específico (`test_importar_csv_com_linha_invalida_nao_derruba_as_validas`) que reproduz o cenário do bug original.

---

## Próximos passos

- [ ] Autenticação com JWT ou API key
- [ ] Rotas de atualização (`PUT`/`PATCH`) e remoção (`DELETE`) de empresas e vagas
- [ ] Frontend simples (Streamlit ou HTML) consumindo a API
- [ ] Paginação também na listagem de vagas

---

## Autor

Desenvolvido por [Guilhermewew](https://github.com/Guilhermewew) — estudante de Análise e Desenvolvimento de Sistemas, com foco em backend Python.
