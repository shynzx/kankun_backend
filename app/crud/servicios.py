from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.servicios import Servicio
from app.schemas.servicios import ServicioCreate, ServicioUpdate

async def get_servicio(db: AsyncSession, servicio_id: int):
    result = await db.execute(select(Servicio).filter(Servicio.id_servicio == servicio_id))
    return result.scalar_one_or_none()

async def get_servicios(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Servicio).offset(skip).limit(limit))
    return result.scalars().all()

async def create_servicio(db: AsyncSession, servicio: ServicioCreate):
    db_servicio = Servicio(**servicio.dict())
    db.add(db_servicio)
    await db.commit()
    await db.refresh(db_servicio)
    return db_servicio

async def update_servicio(db: AsyncSession, servicio_id: int, servicio: ServicioUpdate):
    db_servicio = await get_servicio(db, servicio_id)
    if db_servicio:
        update_data = servicio.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_servicio, key, value)
        await db.commit()
        await db.refresh(db_servicio)
    return db_servicio

async def delete_servicio(db: AsyncSession, servicio_id: int):
    db_servicio = await get_servicio(db, servicio_id)
    if db_servicio:
        await db.delete(db_servicio)
        await db.commit()
        return True
    return False

