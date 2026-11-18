from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
import logging

from app.database.session import get_db
from app.models.client_model import Client
from app.models.event_model import Event

logger = logging.getLogger("uvicorn")

router = APIRouter(tags=["Dashboard"])

# Aponta dinamicamente para 'app/views/templates'
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    """
    Carrega os dados para renderização do painel principal (Dashboard).
    """
    clients = db.query(Client).all()
    events = db.query(Event).options(joinedload(Event.client)).all()
    
    pending_events = (
        db.query(Event)
        .options(joinedload(Event.client))
        .filter(Event.status == "pending")
        .filter(Event.custom_message.isnot(None))
        .all()
    )

    logger.info(f"[Dashboard] {len(clients)} clientes e {len(pending_events)} mensagens pendentes carregadas.")

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "clients": clients,
            "events": events,
            "pending_events": pending_events
        }
    )