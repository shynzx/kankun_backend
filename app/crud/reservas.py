from sqlalchemy.orm import Session
from app.models.reservas import Reserva
from app.schemas.reservas import ReservaCreate, ReservaUpdate

def get_reserva(db: Session, reserva_id: int):
    return db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()

def get_reservas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reserva).offset(skip).limit(limit).all()

def create_reserva(db: Session, reserva: ReservaCreate):
    db_reserva = Reserva(**reserva.dict())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def update_reserva(db: Session, reserva_id: int, reserva: ReservaUpdate):
    db_reserva = get_reserva(db, reserva_id)
    if db_reserva:
        update_data = reserva.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reserva, key, value)
        db.commit()
        db.refresh(db_reserva)
    return db_reserva

def delete_reserva(db: Session, reserva_id: int):
    db_reserva = get_reserva(db, reserva_id)
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
        return True
    return False

