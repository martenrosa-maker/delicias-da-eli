from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    event_date = Column(Date, nullable=False)
    advance_days = Column(Integer, default=7)
    custom_message = Column(String, nullable=True)  # Mensagem gerada pela IA ou personalizada
    
    # Novos campos para o fluxo de aprovação
    status = Column(String, default="pending")  # "pending", "approved", "sent"
    
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="events")