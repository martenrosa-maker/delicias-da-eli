from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
import logging

from app.database.session import get_db
from app.models.client_model import Client

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/clients", tags=["Clients"])

# Schema para receber os dados JSON do fetch
class ClientCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str

@router.post("/", status_code=status.HTTP_201_CREATED)
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_client_json(data: ClientCreateSchema, db: Session = Depends(get_db)):
    """
    Cria um cliente via requisição JSON (usado pelo fetch do dashboard.html).
    """
    # Verifica duplicidade de e-mail
    existing_client = db.query(Client).filter(Client.email == data.email).first()
    if existing_client:
        logger.warning(f"[Clients] Tentativa de cadastro com e-mail duplicado: {data.email}")
        raise HTTPException(
            status_code=400, 
            detail="Este e-mail já está cadastrado para outro cliente."
        )

    try:
        new_client = Client(name=data.name, email=data.email, phone=data.phone)
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        logger.info(f"[Clients] Cliente '{data.name}' cadastrado com sucesso (ID: {new_client.id}).")
        return new_client
    except IntegrityError as e:
        db.rollback()
        logger.error(f"[Clients] Erro de integridade ao salvar cliente: {str(e)}")
        raise HTTPException(
            status_code=400, 
            detail="Erro de integridade ao salvar cliente no banco de dados."
        )

@router.delete("/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    """
    Exclui um cliente e os seus eventos associados.
    """
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    
    db.delete(client)
    db.commit()
    logger.info(f"[Clients] Cliente ID {client_id} excluído.")
    return {"message": "Cliente excluído com sucesso."}