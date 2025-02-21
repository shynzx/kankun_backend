from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tours import Tour
from app.schemas.tours import TourCreate, TourUpdate

async def get_tour(db: AsyncSession, tour_id: int):
    result = await db.execute(select(Tour).filter(Tour.id_tour == tour_id))
    return result.scalars().first()

async def get_tours(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Tour).offset(skip).limit(limit))
    return result.scalars().all()

async def create_tour(db: AsyncSession, tour: TourCreate):
    db_tour = Tour(**tour.dict())
    db.add(db_tour)
    await db.commit()
    await db.refresh(db_tour)
    return db_tour

async def update_tour(db: AsyncSession, tour_id: int, tour: TourUpdate):
    db_tour = await get_tour(db, tour_id)
    if db_tour:
        update_data = tour.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tour, key, value)
        await db.commit()
        await db.refresh(db_tour)
    return db_tour

async def delete_tour(db: AsyncSession, tour_id: int):
    db_tour = await get_tour(db, tour_id)
    if db_tour:
        await db.delete(db_tour)
        await db.commit()
        return True
    return False