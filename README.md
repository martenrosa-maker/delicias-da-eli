# MartenSmart — Gestão de Relacionamento e Automação de Marketing com IA para Confeitarias

Sistema web desenvolvido para a confeitaria **Delícias da Eli** como Projeto Tecnológico do Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas (ULBRA). A plataforma automatiza o acompanhamento de datas comemorativas de clientes, gera mensagens personalizadas por meio de Inteligência Artificial (Google Gemini) e realiza disparos via **WhatsApp Cloud API (Meta)** após revisão humana no painel administrativo.

---

## Tecnologias e Versões Utilizadas

* **Linguagem:** Python 3.12+
* **Framework Web & API:** FastAPI + Uvicorn (ASGI)
* **Banco de Dados:** PostgreSQL 15+ com ORM SQLAlchemy (`psycopg2-binary`)
* **Inteligência Artificial:** Google Gemini API (`google-generativeai`)
* **Mensageria Oficial:** WhatsApp Business Cloud API (Meta Graph API v25.0)
* **Agendamento de Tarefas:** APScheduler (rotina diária às 08h00)
* **Front-end:** HTML5, CSS3, Bootstrap 5 e Jinja2 Templates

---

## Arquitetura do Projeto

O sistema segue uma arquitetura em camadas inspirada no padrão **MVC + Repository-Service**:

```text
marten_smart/
├── app/
│   ├── config/          # Carregamento de variáveis de ambiente (settings.py)
│   ├── controllers/     # Rotas e endpoints REST (clients, events)
│   ├── database/        # Engine, sessão SQLAlchemy e Base declarativa
│   ├── models/          # Entidades relacionais (Client, Event)
│   ├── repositories/    # Camada de acesso e persistência de dados
│   ├── schemas/         # Validação de entrada/saída com Pydantic
│   ├── services/        # Regras de negócio, IA (Gemini), WhatsApp (Meta) e Agendador
│   └── views/           # Templates HTML, CSS e scripts do Dashboard
├── database/
│   └── schema.sql       # Script DDL de criação das tabelas e dados iniciais
├── .env.example         # Modelo de variáveis de ambiente (sem credenciais reais)
├── .gitignore           # Exclusão de arquivos sensíveis e ambiente virtual
└── requirements.txt     # Dependências Python do projeto