import os
from dotenv import load_dotenv

# Carrega as variáveis declaradas no arquivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "MartenSmart System"
    PROJECT_VERSION: str = "1.0.0"
    
    # URL de conexão com o PostgreSQL
    # Exemplo: postgresql://usuario:senha@localhost:5432/nome_do_banco
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/martensmart_db")

settings = Settings()