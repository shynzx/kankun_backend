from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.db_connect import get_session
from app.schemas.payments import (
    PaymentCreate, 
    PaymentResponse, 
    PaymentStatus,
    CustomerCreate,
    CustomerResponse,
    PriceCreate,
    PriceResponse,
    ApiResponse
)
from app.models.pagos import Pago
from app.models.usuarios import Usuario
from app.models.tours import Tour
import stripe
import os
from datetime import datetime

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def create_stripe_customer(customer: CustomerCreate):
    try:
        stripe_customer = stripe.Customer.create(
            name=customer.name,
            email=customer.email
        )
        
        return CustomerResponse(
            customer_id=stripe_customer.id,
            email=stripe_customer.email,
            name=stripe_customer.name
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def create_stripe_price(price: PriceCreate):
    try:
        product = stripe.Product.create(
            name=price.name,
            description=price.description
        )
        
        stripe_price = stripe.Price.create(
            product=product.id,
            unit_amount=int(price.amount * 100),
            currency=price.currency
        )
        
        return PriceResponse(
            price_id=stripe_price.id,
            product_id=product.id,
            amount=price.amount,
            currency=price.currency
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def create_payment_session(db: AsyncSession, payment: PaymentCreate):
    try:
        # Obtener usuario y tour de la base de datos
        usuario = await db.execute(select(Usuario).where(Usuario.id_usuario == payment.id_usuario))
        usuario = usuario.scalar_one_or_none()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        tour = await db.execute(select(Tour).where(Tour.id_tour == payment.id_tour))
        tour = tour.scalar_one_or_none()
        if not tour:
            raise HTTPException(status_code=404, detail="Tour no encontrado")

        if not usuario.stripe_customer_id:
            raise HTTPException(status_code=400, detail="Usuario no tiene ID de cliente de Stripe")
        if not tour.stripe_price_id:
            raise HTTPException(status_code=400, detail="Tour no tiene ID de precio de Stripe")

        # Crear sesión de checkout con Stripe
        session = stripe.checkout.Session.create(
            customer=usuario.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': tour.stripe_price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5173/cancel',
        )

        # Calcular IVA (16%)
        costo_total = float(tour.costo_tour)
        iva = costo_total * 0.16

        # Crear registro de pago en la base de datos
        db_payment = Pago(
            stripe_session_id=session.id,
            stripe_customer_id=usuario.stripe_customer_id,
            stripe_price_id=tour.stripe_price_id,
            metodo_pago='card',
            iva_pago=iva,
            estado_pago='pending',  # Inicialmente pending
            costo_total_pago=costo_total + iva,
            fecha_pago=datetime.utcnow(),
            id_usuario=usuario.id_usuario,
            id_tour=tour.id_tour
        )
        
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)

        return PaymentResponse(
            session_id=session.id,
            checkout_url=session.url
        )

    except stripe.error.StripeError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_payment_status(db: AsyncSession, session_id: str):
    try:
        # Retrieve the session from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Get the payment from our database
        payment = await db.execute(
            select(Pago).where(Pago.stripe_session_id == session_id)
        )
        db_payment = payment.scalar_one_or_none()

        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        # Update payment status in database if it's different
        if session.payment_status == 'paid' and db_payment.estado_pago == 'pending':
            await db.execute(
                update(Pago)
                .where(Pago.stripe_session_id == session_id)
                .values(estado_pago='completed')
            )
            await db.commit()
            # Refresh the payment object to get updated status
            await db.refresh(db_payment)

        return PaymentStatus(
            status=db_payment.estado_pago,
            amount=db_payment.costo_total_pago,
            currency='mxn',
            created_at=db_payment.fecha_pago
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))