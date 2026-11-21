import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

# Define o caminho absoluto para o arquivo .env na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

# Carrega o .env local caso exista (sem sobrescrever variáveis já definidas no Render)
load_dotenv(dotenv_path=env_path, override=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

from app.config.settings import settings
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

# Configura pasta de templates (verifica app/views/templates ou app/templates)
templates_dir = BASE_DIR / "app" / "views" / "templates"
if not templates_dir.exists():
    templates_dir = BASE_DIR / "app" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Middleware global de proteção de rotas: exige login para acessar qualquer página/API protegida
@app.middleware("http")
async def auth_guard_middleware(request: Request, call_next):
    public_paths = ("/login", "/logout", "/static", "/favicon.ico")
    path = request.url.path

    if path.startswith(public_paths):
        return await call_next(request)

    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login", status_code=302)

    return await call_next(request)

# Ativa sessões assinadas por cookie (deve ficar abaixo do auth_guard_middleware para executar antes dele)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

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
async def root(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/dashboard", status_code=302)
    return RedirectResponse(url="/login", status_code=302)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/dashboard", status_code=302)
    #return templates.TemplateResponse("login.html", {"request": request, "error": None})
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == settings.ADMIN_USER and password == settings.ADMIN_PASSWORD:
        request.session["authenticated"] = True
        request.session["user"] = username
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse(
        request,
        "login.html",
        {"error": "Usuário ou senha inválidos."},
        status_code=401,
)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)