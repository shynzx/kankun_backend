from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connect import get_session
from app.crud import payments as payments_crud
from app.schemas.payments import (
    PaymentCreate, 
    PaymentResponse, 
    PaymentStatus, 
    ApiResponse,
    CustomerCreate,
    PriceCreate
)

router = APIRouter(prefix='/api', tags=['Payments'])

@router.post("/customers", response_model=ApiResponse)
async def create_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        result = await payments_crud.create_stripe_customer(customer)
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Customer created successfully"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Failed to create customer"
        )

@router.post("/prices", response_model=ApiResponse)
async def create_price(
    price: PriceCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        result = await payments_crud.create_stripe_price(price)
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Price created successfully"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Failed to create price"
        )

@router.post("/payments", response_model=ApiResponse)
async def create_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_session)
):
    try:
        result = await payments_crud.create_payment_session(db, payment)
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Payment session created successfully"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Failed to create payment session"
        )

@router.get("/payments/{session_id}", response_model=ApiResponse)
async def get_payment_status(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    try:
        result = await payments_crud.get_payment_status(db, session_id)
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Payment status retrieved successfully"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Failed to retrieve payment status"
        )