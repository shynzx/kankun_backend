from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.reservas import ReservaModule
from app.schemas.reservas import Reserva, ReservaCreate, ReservaUpdate
from app.database import get_db

router = APIRouter()

@router.post("/reservas/", response_model=Reserva)
def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    return ReservaModule.create_reserva(db=db, reserva=reserva)

@router.get("/reservas/", response_model=List[Reserva])
def read_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ReservaModule.get_reservas(db, skip=skip, limit=limit)

@router.get("/reservas/{reserva_id}", response_model=Reserva)
def read_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = ReservaModule.get_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.put("/reservas/{reserva_id}", response_model=Reserva)
def update_reserva(reserva_id: int, reserva: ReservaUpdate, db: Session = Depends(get_db)):
    db_reserva = ReservaModule.update_reserva(db, reserva_id=reserva_id, reserva=reserva)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.delete("/reservas/{reserva_id}", response_model=Reserva)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = ReservaModule.delete_reserva(db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.post("/reservas/{reserva_id}/confirm")
def confirm_reserva(reserva_id: int, db: Session = Depends(get_db)):
    return ReservaModule.confirm_reservation(db, reserva_id)

@router.post("/reservas/{reserva_id}/cancel")
def cancel_reserva(reserva_id: int, db: Session = Depends(get_db)):
    return ReservaModule.cancel_reservation(db, reserva_id)