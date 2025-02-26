from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
import stripe
import os
from datetime import datetime
from app.models.pagos import Pago
from app.models.reservas import Reserva
from app.models.usuarios import Usuario
from app.models.tours import Tour
from app.schemas.payments import CreatePaymentSession, PaymentResponse
from decimal import Decimal

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def create_payment_session(db: AsyncSession, payment_data: CreatePaymentSession):
    # Get reservation details with related user and tour
    result = await db.execute(
        select(Reserva)
        .options(
            joinedload(Reserva.usuario),
            joinedload(Reserva.tour).joinedload(Tour.servicios)
        )
        .filter(Reserva.id_reserva == payment_data.id_reserva)
    )
    reservation = result.unique().scalar_one_or_none()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if not reservation.stripe_price_id:
        raise HTTPException(status_code=400, detail="Reservation has no associated Stripe price")

    if not reservation.usuario:
        raise HTTPException(status_code=400, detail="No user associated with this reservation")

    if not reservation.usuario.stripe_customer_id:
        raise HTTPException(status_code=400, detail="User has no associated Stripe customer")

    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            customer=reservation.usuario.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': reservation.stripe_price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=payment_data.success_url,
            cancel_url=payment_data.cancel_url,
        )

        # Create payment record with the total cost from reservation
        payment = Pago(
            stripe_session_id=session.id,
            stripe_customer_id=reservation.usuario.stripe_customer_id,
            stripe_price_id=reservation.stripe_price_id,
            metodo_pago='card',
            iva_pago=float(reservation.costo_reserva) * 0.16,  # IVA component
            estado_pago='pending',
            costo_total_pago=float(reservation.costo_reserva),  # Total cost including IVA
            fecha_pago=datetime.utcnow(),
            id_usuario=reservation.id_usuario,
            id_tour=reservation.id_tour
        )

        db.add(payment)
        await db.commit()
        await db.refresh(payment)

        return {
            "payment": payment,
            "session_url": session.url
        }

    except stripe.error.StripeError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

async def get_payment_status(db: AsyncSession, payment_id: int):
    try:
        result = await db.execute(
            select(Pago).filter(Pago.id_pago == payment_id)
        )
        payment = result.scalar_one_or_none()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        # Get latest status from Stripe
        session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
        
        # Update payment status if changed
        if session.payment_status != payment.estado_pago:
            payment.estado_pago = session.payment_status
            await db.commit()
            await db.refresh(payment)

        return payment

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def refund_payment(db: AsyncSession, payment_id: int, reason: str = None):
    try:
        result = await db.execute(
            select(Pago).filter(Pago.id_pago == payment_id)
        )
        payment = result.scalar_one_or_none()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.estado_pago != 'completed':
            raise HTTPException(status_code=400, detail="Payment must be completed to be refunded")

        # Get payment intent from session
        session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
        payment_intent = session.payment_intent

        # Create refund
        refund = stripe.Refund.create(
            payment_intent=payment_intent,
            reason=reason if reason else 'requested_by_customer'
        )

        # Update payment status
        payment.estado_pago = 'refunded'
        await db.commit()
        await db.refresh(payment)

        return payment

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))