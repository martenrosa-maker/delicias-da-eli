from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Schema Base: Atributos compartilhados
class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo do cliente")
    email: EmailStr = Field(..., description="E-mail válido do cliente")
    phone: str = Field(..., min_length=8, max_length=20, description="Telefone/WhatsApp com DDD")

# Schema para Criação: Dados exigidos na requisição (POST)
class ClientCreate(ClientBase):
    pass

# Schema para Atualização: Todos os campos são opcionais (PUT/PATCH)
class ClientUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=8, max_length=20)

# Schema de Resposta: Dados retornados pela API/View (inclui ID e Data de Criação)
class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permite mapeamento direto de objetos ORM do SQLAlchemy