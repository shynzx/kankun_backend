from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connect import get_session
from app.crud.payments import create_payment_session, get_payment_status, refund_payment
from app.schemas.payments import CreatePaymentSession, PaymentResponse, RefundRequest

router = APIRouter(prefix='/payments', tags=['Payments'])

@router.post("/create-session", summary="Create a payment session")
async def create_session(
    payment_data: CreatePaymentSession,
    db: AsyncSession = Depends(get_session)
):
    """
    Creates a new payment session for a reservation:

    - **id_reserva**: ID of the reservation to pay for
    - **success_url**: URL to redirect after successful payment
    - **cancel_url**: URL to redirect if payment is cancelled

    Returns the payment object and Stripe checkout session URL
    """
    return await create_payment_session(db, payment_data)

@router.get("/{payment_id}/status", response_model=PaymentResponse, summary="Get payment status")
async def check_payment_status(
    payment_id: int,
    db: AsyncSession = Depends(get_session)
):
    """
    Get the current status of a payment:

    - **payment_id**: ID of the payment to check

    Returns the payment object with current status
    """
    return await get_payment_status(db, payment_id)

@router.post("/{payment_id}/refund", response_model=PaymentResponse, summary="Refund a payment")
async def create_refund(
    payment_id: int,
    refund_data: RefundRequest,
    db: AsyncSession = Depends(get_session)
):
    """
    Refund a completed payment:

    - **payment_id**: ID of the payment to refund
    - **reason**: Optional reason for the refund

    Returns the updated payment object
    """
    return await refund_payment(db, payment_id, refund_data.reason)