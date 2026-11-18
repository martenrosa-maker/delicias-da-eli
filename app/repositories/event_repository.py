from sqlalchemy.orm import Session
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, event_data: EventCreate) -> Event:
        db_event = Event(**event_data.model_dump())
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_by_client_id(self, client_id: int):
        return self.db.query(Event).filter(Event.client_id == client_id).all()

