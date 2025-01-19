from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.database import get_session
from app.models.receita import Receita

router = APIRouter(prefix="/receitas", tags=["Receitas"])

# Rota para listar todas as receitas
@router.get("/", response_model=List[Receita], tags=["Receitas"])
def listar_receitas(session: Session = Depends(get_session)):
    try:
        receitas = session.exec(select(Receita)).all()
        return receitas
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar receitas"
        ) from e

# Rota para criar uma nova receita
@router.post("/", response_model=Receita, tags=["Receitas"])
def criar_receita(receita: Receita, session: Session = Depends(get_session)):
    try:
        session.add(receita)
        session.commit()
        session.refresh(receita)
        return receita
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar receita"
        ) from e

# Rota para obter uma receita específica por ID
@router.get("/{receita_id}", response_model=Receita, tags=["Receitas"])
def obter_receita(receita_id: int, session: Session = Depends(get_session)):
    try:
        receita = session.get(Receita, receita_id)
        if not receita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        return receita
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter receita"
        ) from e

# Rota para atualizar uma receita por ID
@router.put("/{receita_id}", response_model=Receita, tags=["Receitas"])
def atualizar_receita(receita_id: int, receita: Receita, session: Session = Depends(get_session)):
    try:
        receita_existente = session.get(Receita, receita_id)
        if not receita_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        
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
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar receita"
        ) from e

# Rota para deletar uma receita por ID
@router.delete("/{receita_id}", tags=["Receitas"])
def deletar_receita(receita_id: int, session: Session = Depends(get_session)):
    try:
        receita = session.get(Receita, receita_id)
        if not receita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        session.delete(receita)
        session.commit()
        return {"message": "Receita deletada com sucesso"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar receita"
        ) from e
