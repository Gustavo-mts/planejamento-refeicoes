from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.receita_ingrediente import ReceitaIngrediente

class Receita(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    tempo_preparo: int
    descricao: Optional[str] = None
    porcoes: int
    nivel_dificuldade: str
    calorias: int
    instrucoes: str
    
    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="receitas",
        link_model=ReceitaIngrediente  # Tabela intermediária
    )

    planejamentos: List["Planejamento"] = Relationship(back_populates="receita")
