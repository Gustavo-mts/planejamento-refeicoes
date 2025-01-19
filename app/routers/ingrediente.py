from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.ingrediente import Ingrediente

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.get("/", response_model=List[Ingrediente], tags=["Ingredientes"])
def listar_ingredientes(session: Session = Depends(get_session)):
    ingredientes = session.exec(select(Ingrediente)).all()
    return ingredientes

# Rota para criar um novo ingrediente
@router.post("/", response_model=Ingrediente)
def criar_ingrediente(ingrediente: Ingrediente, session: Session = Depends(get_session)):
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente

# Rota para obter um ingrediente específico por ID
@router.get("/{ingrediente_id}", response_model=Ingrediente, tags=["Ingredientes"])
def obter_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    return ingrediente

# Rota para atualizar um ingrediente por ID
@router.put("/{ingrediente_id}", response_model=Ingrediente, tags=["Ingredientes"])
def atualizar_ingrediente(ingrediente_id: int, ingrediente: Ingrediente, session: Session = Depends(get_session)):
    ingrediente_existente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente_existente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    
    # Atualizar os campos do ingrediente existente
    ingrediente_existente.nome = ingrediente.nome
    ingrediente_existente.quantidade = ingrediente.quantidade
    ingrediente_existente.unidade_medida = ingrediente.unidade_medida
    
    session.commit()
    session.refresh(ingrediente_existente)
    return ingrediente_existente

# Rota para deletar um ingrediente por ID
@router.delete("/{ingrediente_id}", tags=["Ingredientes"])
def deletar_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    session.delete(ingrediente)
    session.commit()
    return {"message": "Ingrediente deletado com sucesso"}