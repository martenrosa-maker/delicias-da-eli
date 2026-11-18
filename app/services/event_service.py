from sqlalchemy.orm import Session
from app.repositories.event_repository import EventRepository
from app.schemas.event_schema import EventCreate

class EventService:
    def __init__(self, db: Session):
        self.repository = EventRepository(db)

    def create_event(self, event_data: EventCreate):
        return self.repository.create(event_data)

    def get_client_events(self, client_id: int):
        return self.repository.get_by_client_id(client_id)

