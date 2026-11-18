import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging

# Define o caminho absoluto para o arquivo .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

# Força o carregamento do .env indicando o caminho explícito
load_dotenv(dotenv_path=env_path, override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

from app.controllers import client_controller, event_controller
from app.views import dashboard_view
from app.database.session import engine
from app.database.base import Base
from app.services.scheduler_service import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Delícias da Eli - Gestão de Eventos e Clientes",
    description="Sistema de gestão de clientes e automação de lembretes via WhatsApp e IA",
    version="1.0.0"
)

static_dir = BASE_DIR / "app" / "views" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(client_controller.router)
app.include_router(event_controller.router)
app.include_router(dashboard_view.router)

@app.on_event("startup")
async def startup_event():
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")
    gemini_key = os.getenv("GEMINI_API_KEY")

    logger.info("=== INICIALIZANDO DELÍCIAS DA ELI API ===")
    logger.info(f"-> Procurando .env em: {env_path}")
    logger.info(f"-> Arquivo .env existe? {env_path.exists()}")
    logger.info(f"-> Gemini API Key configurada: {'SIM' if gemini_key else 'NÃO'}")
    logger.info(f"-> WhatsApp Token configurado: {'SIM' if whatsapp_token else 'NÃO'}")
    logger.info(f"-> WhatsApp Phone ID configurado: {'SIM' if phone_id else 'NÃO'}")

    # Inicia a rotina automática em background (APScheduler)
    try:
        start_scheduler()
    except Exception as e:
        logger.error(f"Erro ao iniciar o agendador automático: {str(e)}")

@app.get("/")
async def root():
    return {"message": "API Delícias da Eli operando normalmente. Acesse /dashboard para o painel."}