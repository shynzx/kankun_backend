from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_connect import get_session
from app.crud import payments as payments_crud
from app.schemas.payments import (
    PaymentCreate, 
    PaymentResponse, 
    PaymentStatus, 
    ApiResponse,
    RefundCreate,
    RefundResponse
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
    - **status**: Estado actual del pago ('pendiente', 'completado', 'fallido', 'cancelado', 'reembolsado')
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

@router.post("/payments/{payment_id}/refund", response_model=ApiResponse,
    summary="Reembolsar un pago",
    response_description="Información del reembolso procesado"
)
async def refund_payment(
    payment_id: str,
    refund_data: RefundCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Procesa el reembolso de un pago completado:

    - **payment_id**: ID de la sesión de pago a reembolsar ("stripe_session_id" en la tabla "Pagos")
    - **reason**: (Opcional) Razón del reembolso
    
    El proceso realiza las siguientes acciones:
    1. Verifica que el pago exista y esté completado
    2. Procesa el reembolso a través de Stripe
    3. Actualiza el estado del pago en la base de datos
    
    Devuelve:
    - **refund_id**: ID del reembolso
    - **amount**: Monto reembolsado
    - **status**: Estado del reembolso
    - **created_at**: Fecha y hora del reembolso
    
    Posibles errores:
    - 404: Pago no encontrado
    - 400: El pago no está en estado completado
    - 400: Error al procesar el reembolso en Stripe
    """
    try:
        result = await payments_crud.refund_payment(db, RefundCreate(payment_id=payment_id, reason=refund_data.reason))
        return ApiResponse(
            success=True,
            data=result.dict(),
            message="Reembolso procesado exitosamente"
        )
    except Exception as e:
        return ApiResponse(
            success=False,
            error={"detail": str(e)},
            message="Error al procesar el reembolso"
        )