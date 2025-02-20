from sqlalchemy.orm import Session
from app.models.servicios import Servicio
from app.schemas.servicios import ServicioCreate, ServicioUpdate

def get_servicio(db: Session, servicio_id: int):
    return db.query(Servicio).filter(Servicio.id_servicio == servicio_id).first()

def get_servicios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Servicio).offset(skip).limit(limit).all()

def create_servicio(db: Session, servicio: ServicioCreate):
    db_servicio = Servicio(**servicio.dict())
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio

def update_servicio(db: Session, servicio_id: int, servicio: ServicioUpdate):
    db_servicio = get_servicio(db, servicio_id)
    if db_servicio:
        update_data = servicio.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_servicio, key, value)
        db.commit()
        db.refresh(db_servicio)
    return db_servicio

def delete_servicio(db: Session, servicio_id: int):
    db_servicio = get_servicio(db, servicio_id)
    if db_servicio:
        db.delete(db_servicio)
        db.commit()
        return True
    return False
