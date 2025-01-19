from sqlmodel import SQLModel, create_engine, Session
from app.config import settings
from app.models.ingrediente import Ingrediente
from app.models.receita import Receita
from app.models.planejamento import Planejamento
from app.models.receita_ingrediente import ReceitaIngrediente

engine = create_engine(settings.database_url)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
