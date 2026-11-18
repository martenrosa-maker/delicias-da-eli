from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.settings import settings

# 1. Cria a Engine do SQLAlchemy responsável pela conexão com o PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica se a conexão com o banco está ativa antes de usá-la
    echo=False            # Defina como True se quiser ver os SQLs gerados no terminal
)

# 2. Cria a fábrica de sessões (SessionMaker)
# autocommit=False e autoflush=False garantem o controle explícito de transações no Service/Repository
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 3. Função de Injeção de Dependência para obter a sessão do banco por requisição
def get_db() -> Generator[Session, None, None]:
    """
    Gera uma sessão de banco de dados para a requisição HTTP
    e garante que ela seja fechada após o término, mesmo se ocorrer um erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()