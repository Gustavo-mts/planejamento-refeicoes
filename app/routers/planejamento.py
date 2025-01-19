from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from datetime import datetime
from app.models.planejamento import Planejamento
from app.models.planejamento import PlanejamentoCreate

router = APIRouter(prefix="/planejamentos", tags=["Planejamentos"])

# Rota para listar todos os planejamentos
@router.get("/", response_model=List[Planejamento], tags=["Planejamentos"])
def listar_planejamentos(session: Session = Depends(get_session)):
    planejamentos = session.exec(select(Planejamento)).all()
    return planejamentos

# Rota para criar um novo planejamento
@router.post("/", response_model=Planejamento, tags=["Planejamentos"])
def criar_planejamento(
    planejamento_data: PlanejamentoCreate, session: Session = Depends(get_session)
):
    # Converter data de string para objeto date
    planejamento = Planejamento(
        data=datetime.strptime(planejamento_data.data, "%Y-%m-%d").date(),
        receita_id=planejamento_data.receita_id,
        refeicao=planejamento_data.refeicao,
    )
    session.add(planejamento)
    session.commit()
    session.refresh(planejamento)
    return planejamento

# Rota para obter um planejamento específico por ID
@router.get("/{planejamento_id}", response_model=Planejamento, tags=["Planejamentos"])
def obter_planejamento(planejamento_id: int, session: Session = Depends(get_session)):
    planejamento = session.get(Planejamento, planejamento_id)
    if not planejamento:
        raise HTTPException(status_code=404, detail="Planejamento não encontrado")
    return planejamento

# Rota para atualizar um planejamento por ID
@router.put("/{planejamento_id}", response_model=Planejamento, tags=["Planejamentos"])
def atualizar_planejamento(planejamento_id: int, planejamento: Planejamento, session: Session = Depends(get_session)):
    planejamento_existente = session.get(Planejamento, planejamento_id)
    if not planejamento_existente:
        raise HTTPException(status_code=404, detail="Planejamento não encontrado")
    
    # Atualizar os campos do planejamento existente
    planejamento_existente.data = planejamento.data
    planejamento_existente.receita_id = planejamento.receita_id
    
    session.commit()
    session.refresh(planejamento_existente)
    return planejamento_existente

# Rota para deletar um planejamento por ID
@router.delete("/{planejamento_id}", tags=["Planejamentos"])
def deletar_planejamento(planejamento_id: int, session: Session = Depends(get_session)):
    planejamento = session.get(Planejamento, planejamento_id)
    if not planejamento:
        raise HTTPException(status_code=404, detail="Planejamento não encontrado")
    session.delete(planejamento)
    session.commit()
    return {"message": "Planejamento deletado com sucesso"}