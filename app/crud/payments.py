from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.db_connect import get_session
from app.schemas.payments import (
    PaymentCreate, 
    PaymentResponse, 
    PaymentStatus,
    CustomerCreate,
    PriceResponse,
    PriceCreate,
    ApiResponse,
    RefundCreate,
    RefundResponse
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

async def update_payment_status(db: AsyncSession, session_id: str, new_status: str):
    try:
        stmt = (
            update(Pago)
            .where(Pago.stripe_session_id == session_id)
            .values(estado_pago=new_status)
        )
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating payment status: {str(e)}")

async def check_session_status(db: AsyncSession, session_id: str):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        payment_status = session.payment_status
        
        # Mapear estados de Stripe a nuestros estados
        stripe_to_db_status = {
            'paid': 'completado',
            'unpaid': 'pendiente',
            'canceled': 'cancelado',
            'expired': 'fallido'
        }
        
        new_status = stripe_to_db_status.get(payment_status, 'pendiente')
        await update_payment_status(db, session_id, new_status)
        
        return new_status
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
            payment_intent_data={
                'setup_future_usage': 'off_session'
            }
        )

        costo_total = float(tour.costo_tour)
        # Calcular el IVA que ya está incluido (16% del precio total)
        # Para obtener el IVA de un precio que ya lo incluye: precio * 0.16 / 1.16
        iva = costo_total * (0.16 / 1.16)

        # Crear registro de pago en la base de datos
        db_payment = Pago(
            stripe_session_id=session.id,
            stripe_customer_id=usuario.stripe_customer_id,
            stripe_price_id=tour.stripe_price_id,
            metodo_pago='card',
            iva_pago=iva,
            estado_pago='pending',  # Inicialmente pending
            costo_total_pago=costo_total,
            fecha_pago=datetime.utcnow(),
            id_usuario=usuario.id_usuario,
            id_tour=tour.id_tour
        )
        
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)

        # Verificar el estado inicial del pago
        await check_session_status(db, session.id)

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
        # Verificar y actualizar el estado del pago
        new_status = await check_session_status(db, session_id)
        
        # Obtener el pago actualizado de la base de datos
        result = await db.execute(
            select(Pago).where(Pago.stripe_session_id == session_id)
        )
        db_payment = result.scalar_one_or_none()

        if not db_payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        return PaymentStatus(
            status=new_status,
            amount=db_payment.costo_total_pago,
            currency='mxn',
            created_at=db_payment.fecha_pago
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def refund_payment(db: AsyncSession, refund_data: RefundCreate):
    try:
        # Obtener el pago de la base de datos
        result = await db.execute(
            select(Pago).where(Pago.stripe_session_id == refund_data.payment_id)
        )
        db_payment = result.scalar_one_or_none()

        if not db_payment:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        if db_payment.estado_pago != 'completado':
            raise HTTPException(status_code=400, detail="Solo se pueden reembolsar pagos completados")

        # Obtener la sesión de Stripe
        session = stripe.checkout.Session.retrieve(refund_data.payment_id)
        payment_intent = session.payment_intent

        # Crear el reembolso en Stripe
        refund = stripe.Refund.create(
            payment_intent=payment_intent,
            reason=refund_data.reason if refund_data.reason else 'requested_by_customer'
        )

        # Actualizar el estado del pago en la base de datos
        await update_payment_status(db, refund_data.payment_id, 'reembolsado')

        return RefundResponse(
            refund_id=refund.id,
            amount=float(refund.amount) / 100,  # Convertir de centavos a la moneda base
            status=refund.status,
            created_at=datetime.fromtimestamp(refund.created)
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))