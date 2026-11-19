import os
from dotenv import load_dotenv

# Carrega as variáveis declaradas no arquivo .env (ambiente local)
load_dotenv()


def _get_database_url() -> str:
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/martensmart_db",
    ).strip()

    # Normaliza prefixos padrão de provedores em nuvem (Neon / Render) para o driver psycopg v3
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


class Settings:
    PROJECT_NAME: str = "Delícias da Eli - CRM & Automação"
    PROJECT_VERSION: str = "1.0.0"

    # URL de conexão com o PostgreSQL
    DATABASE_URL: str = _get_database_url()

    # Credenciais das integrações externas (Google Gemini e Meta Cloud API)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID: str = os.getenv("WHATSAPP_PHONE_ID", "")


settings = Settings()