from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
import logging

from app.database.session import get_db
from app.models.event_model import Event
from app.services.evolution_service import EvolutionService
from app.services.ai_service import AIService

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/events", tags=["Events"])

# Schema para receber os dados JSON do evento
class EventCreateSchema(BaseModel):
    title: str
    event_date: date
    advance_days: int = 7
    custom_message: Optional[str] = None
    client_id: int

@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_event(data: EventCreateSchema, db: Session = Depends(get_db)):
    """
    Cria um evento associado a um cliente.
    """
    new_event = Event(
        title=data.title,
        event_date=data.event_date,
        advance_days=data.advance_days,
        custom_message=data.custom_message,
        client_id=data.client_id,
        status="pending"
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    logger.info(f"[Events] Evento '{data.title}' criado com sucesso para o Cliente ID {data.client_id}.")
    return new_event

@router.post("/trigger-scheduler")
async def trigger_scheduler_manual(db: Session = Depends(get_db)):
    """
    Força a execução manual do gerador de mensagens da IA para todos os eventos pendentes.
    """
    events = db.query(Event).filter(Event.status == "pending").all()
    count = 0

    for event in events:
        if not event.custom_message or event.custom_message.strip() == "":
            try:
                client = event.client
                if not client:
                    continue

                event_date_fmt = event.event_date.strftime('%d/%m/%Y') if event.event_date else ""

                # Chamada alinhada exatamente com os parâmetros do ai_service.py
                draft = await AIService.generate_reminder_message(
                    client_name=client.name,
                    event_name=event.title,
                    event_date=event_date_fmt
                )
                
                event.custom_message = draft
                count += 1
            except Exception as e:
                logger.error(f"[Scheduler Manual] Erro ao gerar mensagem para o evento ID {event.id}: {str(e)}")

    db.commit()
    return {
        "status": "success",
        "message": f"Processamento concluído. {count} mensagens foram geradas pela IA."
    }

@router.post("/{event_id}/approve-and-send")
async def approve_and_send_event_message(event_id: int, db: Session = Depends(get_db)):
    """
    Aprova a mensagem gerada e envia via Evolution API.
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    
    if not event.client or not event.client.phone:
        raise HTTPException(status_code=400, detail="Cliente não possui telefone cadastrado")
    
    event_date_fmt = event.event_date.strftime('%d/%m/%Y') if event.event_date else ""
    
    # Disparo através da Evolution API
    result = EvolutionService.send_event_reminder(
        to_phone=event.client.phone,
        client_name=event.client.name,
        event_name=event.title,
        event_date=event_date_fmt,
        custom_message=event.custom_message
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500, 
            detail=f"Falha ao enviar mensagem pelo WhatsApp: {result.get('error')}"
        )
    
    event.status = "sent"
    db.commit()
    
    return {"message": "Mensagem aprovada e enviada com sucesso!"}