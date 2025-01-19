from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.receita import Receita

router = APIRouter(prefix="/receitas", tags=["Receitas"])

# Rota para listar todas as receitas
@router.get("/", response_model=List[Receita], tags=["Receitas"])
def listar_receitas(session: Session = Depends(get_session)):
    receitas = session.exec(select(Receita)).all()
    return receitas

# Rota para criar uma nova receita
@router.post("/", response_model=Receita, tags=["Receitas"])
def criar_receita(receita: Receita, session: Session = Depends(get_session)):
    session.add(receita)
    session.commit()
    session.refresh(receita)
    return receita

# Rota para obter uma receita específica por ID
@router.get("/{receita_id}", response_model=Receita, tags=["Receitas"])
def obter_receita(receita_id: int, session: Session = Depends(get_session)):
    receita = session.get(Receita, receita_id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return receita

# Rota para atualizar uma receita por ID
@router.put("/{receita_id}", response_model=Receita, tags=["Receitas"])
def atualizar_receita(receita_id: int, receita: Receita, session: Session = Depends(get_session)):
    receita_existente = session.get(Receita, receita_id)
    if not receita_existente:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    
    # Atualizar os campos da receita existente
    receita_existente.nome = receita.nome
    receita_existente.tempo_preparo = receita.tempo_preparo
    receita_existente.descricao = receita.descricao
    receita_existente.porcoes = receita.porcoes
    receita_existente.nivel_dificuldade = receita.nivel_dificuldade
    receita_existente.calorias = receita.calorias
    receita_existente.instrucoes = receita.instrucoes
    
    session.commit()
    session.refresh(receita_existente)
    return receita_existente

# Rota para deletar uma receita por ID
@router.delete("/{receita_id}", tags=["Receitas"])
def deletar_receita(receita_id: int, session: Session = Depends(get_session)):
    receita = session.get(Receita, receita_id)
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    session.delete(receita)
    session.commit()
    return {"message": "Receita deletada com sucesso"}
