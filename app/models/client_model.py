from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    
    # Define o padrão no Python (default) e no banco de dados (server_default)
    created_at = Column(DateTime, default=datetime.now, server_default=func.now(), nullable=False)

    # Relacionamento de 1 para N com Eventos e exclusão em cascata
    events = relationship("Event", back_populates="client", cascade="all, delete-orphan")
    # Define o padrão tanto no Python (default) quanto na instrução do banco (server_default)
    created_at = Column(DateTime, default=datetime.now, server_default=func.now(), nullable=False)

    events = relationship("Event", back_populates="client", cascade="all, delete-orphan")