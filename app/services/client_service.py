from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.client_repository import ClientRepository
from app.schemas.client_schema import ClientCreate

class ClientService:
    def list_all_clients(self):
        return self.get_all_clients()
    def __init__(self, db: Session):
        self.repository = ClientRepository(db)

    def get_all_clients(self):
        return self.repository.get_all()

    def create_client(self, client_data: ClientCreate):
        return self.repository.create(client_data)

    def delete_client(self, client_id: int):
        success = self.repository.delete(client_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID {client_id} não encontrado."
            )
        return {"detail": "Cliente excluído com sucesso!"}