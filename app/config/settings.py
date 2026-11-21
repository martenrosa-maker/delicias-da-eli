import os
from dotenv import load_dotenv

load_dotenv()


def _get_database_url() -> str:
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/martensmart_db",
    ).strip()

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    return url


class Settings:
    PROJECT_NAME: str = "Delícias da Eli - CRM & Automação"
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL: str = _get_database_url()

    # Credenciais de Acesso ao Painel
    ADMIN_USER: str = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "eli2026")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "delicias-da-eli-chave-secreta-2026")

    # Integrações externas
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    WHATSAPP_TOKEN: str = os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_ID: str = os.getenv("WHATSAPP_PHONE_ID", "")


settings = Settings()
