from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.reservas import Reserva
from app.schemas.reservas import ReservaCreate, ReservaUpdate

async def get_reserva(db: AsyncSession, reserva_id: int):
    result = await db.execute(select(Reserva).filter(Reserva.id_reserva == reserva_id))
    return result.scalar_one_or_none()

async def get_reservas(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Reserva).offset(skip).limit(limit))
    return result.scalars().all()


async def create_reserva(db: AsyncSession, reserva: ReservaCreate):
    db_reserva = Reserva(**reserva.dict())
    db.add(db_reserva)
    await db.commit()
    await db.refresh(db_reserva)
    return db_reserva

async def update_reserva(db: AsyncSession, reserva_id: int, reserva: ReservaUpdate):
    db_reserva = await get_reserva(db, reserva_id)
    if db_reserva:
        update_data = reserva.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reserva, key, value)
        await db.commit()
        await db.refresh(db_reserva)
    return db_reserva

async def delete_reserva(db: AsyncSession, reserva_id: int):
    db_reserva = await get_reserva(db, reserva_id)
    if db_reserva:
        await db.delete(db_reserva)
        await db.commit()
        return True
    return False

