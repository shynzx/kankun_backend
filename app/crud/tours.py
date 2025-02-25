from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.servicios import Servicio
from app.models.tours import Tour
from app.schemas.tours import AddServicioToTour, TourCreate, TourUpdate
from sqlalchemy.orm import selectinload
import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def get_tour(db: AsyncSession, tour_id: int):
    result = await db.execute(select(Tour).filter(Tour.id_tour == tour_id))
    return result.scalars().first()

async def get_tours(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Tour).offset(skip).limit(limit))
    return result.scalars().all()

async def create_tour(db: AsyncSession, tour: TourCreate):
    try:
        # Crear producto en Stripe
        product = stripe.Product.create(
            name=tour.nombre_tour,
            description=tour.descripcion_tour
        )
        
        # Crear precio en Stripe
        price = stripe.Price.create(
            product=product.id,
            unit_amount=int(float(tour.costo_tour) * 100),  # Convertir a centavos
            currency='mxn'  # Usando MXN como moneda por defecto
        )
        
        # Crear tour en la base de datos
        db_tour = Tour(
            nombre_tour=tour.nombre_tour,
            descripcion_tour=tour.descripcion_tour,
            costo_tour=tour.costo_tour,
            dias_tour=tour.dias_tour,
            tipo_tour=tour.tipo_tour,
            maxpersonas_tour=tour.maxpersonas_tour,
            direccion_inicio_tour=tour.direccion_inicio_tour,
            direccion_destino_tour=tour.direccion_destino_tour,
            imagen_tour = tour.imagen_tour,
            stripe_product_id=product.id,
            stripe_price_id=price.id
        )
        
        db.add(db_tour)
        await db.commit()
        await db.refresh(db_tour)
        return db_tour
        
    except stripe.error.StripeError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating Stripe product/price: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise e

async def update_tour(db: AsyncSession, tour_id: int, tour: TourUpdate):
    db_tour = await get_tour(db, tour_id)
    if db_tour:
        try:
            # Actualizar producto en Stripe si es necesario
            if tour.nombre_tour or tour.descripcion_tour:
                stripe.Product.modify(
                    db_tour.stripe_product_id,
                    name=tour.nombre_tour or db_tour.nombre_tour,
                    description=tour.descripcion_tour or db_tour.descripcion_tour
                )
            
            # Si el precio cambió, crear un nuevo precio en Stripe
            if tour.costo_tour:
                new_price = stripe.Price.create(
                    product=db_tour.stripe_product_id,
                    unit_amount=int(float(tour.costo_tour) * 100),
                    currency='mxn'
                )
                db_tour.stripe_price_id = new_price.id
            
            # Actualizar otros campos del tour
            update_data = tour.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_tour, key, value)
                
            await db.commit()
            await db.refresh(db_tour)
            
        except stripe.error.StripeError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Error updating Stripe product/price: {str(e)}")
    return db_tour

async def delete_tour(db: AsyncSession, tour_id: int):
    db_tour = await get_tour(db, tour_id)
    if db_tour:
        try:
            # Archivar el producto en Stripe (no se pueden eliminar productos)
            stripe.Product.modify(
                db_tour.stripe_product_id,
                active=False
            )
            
            # Eliminar el tour de la base de datos
            await db.delete(db_tour)
            await db.commit()
            return True
            
        except stripe.error.StripeError as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Error archiving Stripe product: {str(e)}")
    return False

async def add_servicio_to_tour(db: AsyncSession, tour_id: int, servicio_data: AddServicioToTour):
    result = await db.execute(
        select(Tour).options(selectinload(Tour.servicios)).filter(Tour.id_tour == tour_id)
    )
    db_tour = result.scalars().first()

    if not db_tour:
        raise HTTPException(status_code=404, detail="Tour no encontrtado")

    # Obtener el servicio
    result = await db.execute(select(Servicio).filter(Servicio.id_servicio == servicio_data.id_servicio))
    db_servicio = result.scalars().first()

    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # Verificar si el servicio ya está en el tour
    if db_servicio in db_tour.servicios:
        raise HTTPException(status_code=400, detail="El Servicio ya se encuentra en el Tour")

    # Agregar el servicio al tour
    db_tour.servicios.append(db_servicio)

    try:
        await db.commit()
        await db.refresh(db_tour)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al añadir el servicio: {str(e)}")

    return db_tour