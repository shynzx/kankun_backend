from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr

class CustomerResponse(BaseModel):
    customer_id: str
    email: str
    name: str

class PriceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    currency: str = "mxn"

class PriceResponse(BaseModel):
    price_id: str
    product_id: str
    amount: float
    currency: str

class PaymentCreate(BaseModel):
    id_usuario: int
    id_tour: int

class PaymentResponse(BaseModel):
    session_id: str
    checkout_url: str

class PaymentStatus(BaseModel):
    status: str
    amount: float
    currency: str
    created_at: datetime

class RefundCreate(BaseModel):
    payment_id: str = Field(..., description="ID de la sesión de pago a reembolsar")
    reason: Optional[str] = Field(None, description="Razón del reembolso")

class RefundResponse(BaseModel):
    refund_id: str
    amount: float
    status: str
    created_at: datetime

class ApiResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: str
    error: Optional[dict] = None