from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class EventBase(BaseModel):
    title: str
    event_date: date
    advance_days: int = 7
    custom_message: Optional[str] = None

class EventCreate(EventBase):
    client_id: int

class EventResponse(EventBase):
    id: int
    client_id: int

    model_config = ConfigDict(from_attributes=True)
