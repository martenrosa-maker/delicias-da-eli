from app.database.session import engine, Base
import app.models.client_model
import app.models.event_model

print("Apagando tabelas antigas...")
Base.metadata.drop_all(bind=engine)

print("Criando tabelas atualizadas com a coluna 'status'...")
Base.metadata.create_all(bind=engine)

print("Banco de dados atualizado com sucesso!")
