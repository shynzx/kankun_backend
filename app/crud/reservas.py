from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.reservas import Reserva
from app.models.tours import Tour
from app.schemas.reservas import *
import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def get_reserva(db: AsyncSession, reserva_id: int):
    result = await db.execute(select(Reserva).filter(Reserva.id_reserva == reserva_id))
    return result.scalar_one_or_none()

async def get_reservas(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Reserva).offset(skip).limit(limit))
    return result.scalars().all()

async def create_reserva(db: AsyncSession, reserva: ReservaCreate):
    try:
        # Get tour information
        tour_result = await db.execute(
            select(Tour).filter(Tour.id_tour == reserva.id_tour)
        )
        tour = tour_result.scalar_one_or_none()
        
        if not tour:
            raise ValueError("Tour not found")

        # Create Stripe product
        product = stripe.Product.create(
            name=f"Reserva para {tour.nombre_tour}",
            description=f"Reserva para el tour {tour.nombre_tour} del usuario {reserva.id_usuario}"
        )
        
        # Create Stripe price
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(float(reserva.costo_reserva) * 100),  # Convert to cents
            currency="mxn"
        )
        
        # Create reservation in database
        db_reserva = Reserva(
            id_usuario=reserva.id_usuario,
            id_tour=reserva.id_tour,
            costo_reserva=reserva.costo_reserva,
            estado=reserva.estado,
            stripe_product_id=product.id,
            stripe_price_id=price.id
        )
        
        db.add(db_reserva)
        await db.commit()
        await db.refresh(db_reserva)
        return db_reserva
        
    except Exception as e:
        await db.rollback()
        # Clean up Stripe resources if database operation fails
        if 'product' in locals():
            stripe.Product.delete(product.id)
        raise e

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
        # Delete Stripe product and price
        if db_reserva.stripe_product_id:
            stripe.Product.delete(db_reserva.stripe_product_id)
        
        await db.delete(db_reserva)
        await db.commit()
        return True
    return False

async def cancelar_reserva(db: AsyncSession, reserva_id: int):
    db_reserva = await get_reserva(db, reserva_id)
    if db_reserva:
        db_reserva.estado = EstadoReserva.CANCELADO
        
        # Archive the Stripe product
        if db_reserva.stripe_product_id:
            stripe.Product.modify(
                db_reserva.stripe_product_id,
                active=False
            )
        
        await db.commit()
        await db.refresh(db_reserva)
        return db_reserva
    return None

async def confirmar_reserva(db: AsyncSession, reserva_id: int):
    db_reserva = await get_reserva(db, reserva_id)
    if db_reserva:
        db_reserva.estado = EstadoReserva.ACTIVO
        await db.commit()
        await db.refresh(db_reserva)
        return db_reserva
    return None