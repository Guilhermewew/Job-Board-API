# 🚀 Job Board API

![Python 3.12+ e FastAPI (async](https://img.shields.io/badge/-Python 3.12+ e FastAPI (async-blue?style=flat-square) ![alta performance)

•
Pydantic para validação de dados e schemas (EmpresaCreate](https://img.shields.io/badge/-alta performance)

•
Pydantic para validação de dados e schemas (EmpresaCreate-blue?style=flat-square) ![VagaCreate](https://img.shields.io/badge/-VagaCreate-blue?style=flat-square) ![ValidadorCsv)

•
SQLite como banco de dados (persistência local](https://img.shields.io/badge/-ValidadorCsv)

•
SQLite como banco de dados (persistência local-blue?style=flat-square) ![sem configuração)

•
pytest para testes automatizados

•
Documentação interativa automática (OpenAPI 3.4 / Swagger UI)](https://img.shields.io/badge/-sem configuração)

•
pytest para testes automatizados

•
Documentação interativa automática (OpenAPI 3.4 / Swagger UI)-blue?style=flat-square) 

## 📝 Descrição
API REST para gerenciamento de vagas de emprego e empresas, construída com FastAPI. Permite cadastrar empresas, publicar vagas, importar grandes volumes de vagas por CSV e reimportar dados com validação completa.
O problema que este projeto resolve

Recrutadores e empresas de RH frequentemente recebem dezenas de vagas por e-mail ou planilha, espalhadas em arquivos CSV, sem um lugar central para consultá-las. Esta API resolve isso oferecendo um cadastro estruturado de empresas e vagas, com importação em lote via CSV — o fluxo real que empresas usam para carregar dados históricos.

Funcionalidades

Recurso
Endpoint
Descrição
Empresas
POST /empresas/
Cadastra uma nova empresa
Empresas
GET /empresas/
Lista todas as empresas
Empresas
GET /empresas/{empresa_id}
Consulta uma empresa pelo ID
Vagas
POST /vagas/
Cadastra uma nova vaga
Vagas
GET /vagas/
Lista todas as vagas (com filtros )
Vagas
GET /vagas/{vaga_id}
Consulta uma vaga pelo ID
Importação
POST /vagas/importar-csv/
Importa vagas em lote a partir de um arquivo CSV
Reimportação
POST /vagas/importar-csv/reimportar-id
Reimporta/ajusta uma importação anterior




Tecnologias

•
Python 3.12+ e FastAPI (async, alta performance)

•
Pydantic para validação de dados e schemas (EmpresaCreate, VagaCreate, ValidadorCsv)

•
SQLite como banco de dados (persistência local, sem configuração)

•
pytest para testes automatizados

•
Documentação interativa automática (OpenAPI 3.4 / Swagger UI)

Como rodar localmente

Bash


# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/job-board-api.git
cd job-board-api

# 2. Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
fastapi dev app/main.py

# 5. Acesse a documentação interativa
# http://127.0.0.1:8000/docs



Como testar

Bash


# Executar toda a suíte de testes
pytest

# Com cobertura
pytest --cov=app



Exemplos de uso

Cadastrar uma empresa:

Bash


curl -X POST http://127.0.0.1:8000/empresas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "TechCorp Brasil",
    "setor": "Tecnologia",
    "cidade": "São Paulo"
  }'



Importar vagas por CSV:

Bash


curl -X POST http://127.0.0.1:8000/vagas/importar-csv/ \
  -F "file=@vagas_exemplo.csv"



Formato esperado do CSV:

Plain Text


titulo,cargo,empresa_id,salario,modalidade
Desenvolvedor Python Backend,Desenvolvedor,1,8000,remoto
Analista de Dados Pleno,Analista,1,6000,hibrido



Linhas inválidas são rejeitadas com mensagem clara de erro, sem interromper o restante da importação.

Arquitetura e decisões técnicas

•
FastAPI em vez de Flask/Django: escolhi FastAPI pela validação automática via Pydantic, suporte nativo a async (importante para importações em lote ) e documentação OpenAPI gerada automaticamente — o que reduz trabalho manual e aumenta a confiabilidade dos contratos de API.

•
Schemas separados de entrada e saída (Create vs Response): evita vazar campos internos e permite evoluir o contrato de cada endpoint independentemente.

•
Validação de CSV em duas etapas (ValidadorCsv + ImportacaoCSVVagas): a validação acontece antes de qualquer escrita no banco, garantindo que importações parciais nunca deixem o sistema em estado inconsistente.

•
SQLite para a primeira versão: mantém o projeto rodando sem dependências externas (Docker, PostgreSQL), priorizando simplicidade e reprodutibilidade. Uma migração para PostgreSQL é o próximo passo natural para produção.

Próximos passos




Autenticação com JWT (empresas gerenciam apenas as próprias vagas)




Migração para PostgreSQL




Importação em background (BackgroundTasks/Celery) para arquivos grandes




Frontend simples com Streamlit consumindo a API

Sobre o autor

Desenvolvedor Python em formação, focado em backend e dados. Este projeto faz parte de um portfólio construído para demonstrar domínio de REST, validação, testes e deploy.




Feito com FastAPI e muito café.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.12+ e FastAPI (async**
- **alta performance)

•
Pydantic para validação de dados e schemas (EmpresaCreate**
- **VagaCreate**
- **ValidadorCsv)

•
SQLite como banco de dados (persistência local**
- **sem configuração)

•
pytest para testes automatizados

•
Documentação interativa automática (OpenAPI 3.4 / Swagger UI)**

---

## 💻 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/](https://github.com/)Guilhemewew/Job Board API.git
   ```

2. **Entre no diretório:**
   ```bash
   cd Job Board API
   ```

---

## 👤 Autor
Desenvolvido por [Guilhemewew](https://github.com/Guilhemewew).