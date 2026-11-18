import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.event_service import EventService
from app.database.session import SessionLocal

logger = logging.getLogger("uvicorn")
scheduler = AsyncIOScheduler()

def run_daily_ai_drafts():
    """
    Busca eventos próximos e gera as mensagens com IA automaticamente.
    """
    logger.info("[Scheduler] Executando rotina diária de geração de mensagens via IA...")
    db = SessionLocal()
    try:
        # Chama a mesma lógica de negócio usada no trigger-scheduler
        events_processed = EventService.process_upcoming_events_ai(db)
        logger.info(f"[Scheduler] Sucesso! {events_processed} mensagens rascunhadas pela IA.")
    except Exception as e:
        logger.error(f"[Scheduler] Erro ao processar rascunhos de IA: {str(e)}")
    finally:
        db.close()

def start_scheduler():
    """
    Inicia o agendador de tarefas em segundo plano.
    Configurado para rodar todos os dias às 08:00 AM.
    """
    # Agenda para rodar diariamente às 08:00
    scheduler.add_job(run_daily_ai_drafts, 'cron', hour=8, minute=0)
    scheduler.start()
    logger.info("[Scheduler] Agendador automático iniciado (Execução diária às 08:00).")