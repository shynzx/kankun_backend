from sqlalchemy.orm import Session
from app.models.tours import Tour
from app.schemas.tours import TourCreate, TourUpdate

def get_tour(db: Session, tour_id: int):
    return db.query(Tour).filter(Tour.id_tour == tour_id).first()

def get_tours(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tour).offset(skip).limit(limit).all()

def create_tour(db: Session, tour: TourCreate):
    db_tour = Tour(**tour.dict())
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour

def update_tour(db: Session, tour_id: int, tour: TourUpdate):
    db_tour = get_tour(db, tour_id)
    if db_tour:
        update_data = tour.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tour, key, value)
        db.commit()
        db.refresh(db_tour)
    return db_tour

def delete_tour(db: Session, tour_id: int):
    db_tour = get_tour(db, tour_id)
    if db_tour:
        db.delete(db_tour)
        db.commit()
        return True
    return False

