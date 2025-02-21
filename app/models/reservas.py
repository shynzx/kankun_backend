from sqlalchemy.orm import Session
from app.crud import reserva as reserva_crud
from app.schemas.reservas import ReservaCreate, ReservaUpdate
from app.models.reservas import Reserva

class ReservaModule:
    @staticmethod
    def create_reserva(db: Session, reserva: ReservaCreate):
        return reserva_crud.create_reserva(db=db, reserva=reserva)

    @staticmethod
    def get_reservas(db: Session, skip: int = 0, limit: int = 100):
        return reserva_crud.get_reservas(db, skip=skip, limit=limit)

    @staticmethod
    def get_reserva(db: Session, reserva_id: int):
        return reserva_crud.get_reserva(db, reserva_id=reserva_id)

    @staticmethod
    def update_reserva(db: Session, reserva_id: int, reserva: ReservaUpdate):
        return reserva_crud.update_reserva(db, reserva_id=reserva_id, reserva=reserva)

    @staticmethod
    def delete_reserva(db: Session, reserva_id: int):
        return reserva_crud.delete_reserva(db, reserva_id=reserva_id)

    @staticmethod
    def check_availability(db: Session, id_tour: int, fecha: str):
        pass

    @staticmethod
    def calculate_total_cost(db: Session, id_tour: int, num_personas: int):
        pass

    @staticmethod
    def confirm_reservation(db: Session, reserva_id: int):
        reserva = reserva_crud.get_reserva(db, reserva_id)
        if reserva:
            reserva.estatus = 'confirmado'
            db.commit()
        return reserva

    @staticmethod
    def cancel_reservation(db: Session, reserva_id: int):
        reserva = reserva_crud.get_reserva(db, reserva_id)
        if reserva:
            reserva.estatus = 'cancelado'
            db.commit()
        return reserva