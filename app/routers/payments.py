from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connect import get_session
from app.crud import payments as payments_crud
from app.schemas.payments import (
    PaymentCreate, 
    PaymentResponse, 
    PaymentStatus, 
    ApiResponse
)

router = APIRouter(prefix='/api', tags=['Payments'])

@router.post("/payments", response_model=ApiResponse,
    summary="Crear una nueva sesión de pago",
    response_description="Información de la sesión de pago creada"
)
async def create_payment(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Crea una nueva sesión de pago en Stripe para procesar el pago de un tour:

    - **id_usuario**: ID del usuario que realizará el pago
    - **id_tour**: ID del tour que se desea comprar
    
    El proceso realiza las siguientes acciones:
    1. Verifica la existencia del usuario y el tour
    2. Valida que el usuario tenga un ID de cliente en Stripe
    3. Valida que el tour tenga un precio configurado en Stripe
    4. Crea una sesión de pago en Stripe
    5. Registra el pago en la base de datos
    
    Devuelve:
    - **session_id**: ID de la sesión de pago
    - **checkout_url**: URL para realizar el pago
    """
    try:
        result = await payments_crud.create_payment_session(db, payment)
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Sesión de pago creada exitosamente"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Error al crear la sesión de pago"
        )

@router.get("/payments/{session_id}", response_model=ApiResponse,
    summary="Consultar estado de un pago",
    response_description="Estado actual del pago"
)
async def get_payment_status(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Obtiene el estado actual de un pago utilizando su ID de sesión:

    - **session_id**: ID de la sesión de pago de Stripe
    
    Devuelve:
    - **status**: Estado actual del pago ('pending', 'completed', 'failed', 'cancelled')
    - **amount**: Monto total del pago
    - **currency**: Moneda del pago
    - **created_at**: Fecha y hora de creación del pago
    """
    try:
        result = await payments_crud.get_payment_status(db, session_id)
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Estado del pago recuperado exitosamente"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Error al obtener el estado del pago"
        )