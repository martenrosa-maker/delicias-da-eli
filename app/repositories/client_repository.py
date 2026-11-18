from sqlalchemy.orm import Session
from app.models.client_model import Client

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Client).all()

    def get_by_id(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def create(self, client_data):
        client = Client(**client_data.model_dump())
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client_id: int) -> bool:
        client = self.get_by_id(client_id)
        if client:
            self.db.delete(client)
            self.db.commit()
            return True
        return False