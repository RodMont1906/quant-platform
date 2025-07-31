from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.data.models import Strategy
from src.infrastructure.db.session import get_db

router = APIRouter()


class StrategyCreate(BaseModel):
    name: str
    parameters: dict
    portfolio_id: UUID


class StrategyOut(StrategyCreate):
    id: UUID


@router.post("/", response_model=StrategyOut)
def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = Strategy(**strategy.dict())
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy


@router.get("/", response_model=List[StrategyOut])
def list_strategies(db: Session = Depends(get_db)):
    return db.query(Strategy).all()


@router.get("/{strategy_id}", response_model=StrategyOut)
def get_strategy(strategy_id: UUID, db: Session = Depends(get_db)):
    strategy = db.query(Strategy).get(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.put("/{strategy_id}", response_model=StrategyOut)
def update_strategy(
    strategy_id: UUID, strategy: StrategyCreate, db: Session = Depends(get_db)
):
    db_strategy = db.query(Strategy).get(strategy_id)
    if not db_strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    for key, value in strategy.dict().items():
        setattr(db_strategy, key, value)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy


@router.delete("/{strategy_id}")
def delete_strategy(strategy_id: UUID, db: Session = Depends(get_db)):
    db_strategy = db.query(Strategy).get(strategy_id)
    if not db_strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    db.delete(db_strategy)
    db.commit()
    return {"message": "Strategy deleted"}
