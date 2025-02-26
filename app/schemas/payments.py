from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class CreatePaymentSession(BaseModel):
    id_reserva: int
    success_url: str 
    cancel_url: str

class PaymentResponse(BaseModel):
    id_pago: int
    stripe_session_id: str
    stripe_customer_id: str
    stripe_price_id: str
    metodo_pago: str
    iva_pago: float
    estado_pago: str
    costo_total_pago: float
    fecha_pago: datetime
    id_usuario: int
    id_tour: int

    class Config:
        from_attributes = True

class RefundRequest(BaseModel):
    id_pago: int
    reason: Optional[str] = None