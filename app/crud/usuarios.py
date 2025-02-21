from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuarios import Usuario
from app.schemas.usuarios import crear_usuario
from passlib.context import CryptContext
import stripe
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

async def get_usuario_by_email(session: AsyncSession, correo_usuario: str):
    stmt = select(Usuario).where(Usuario.correo_usuario == correo_usuario)
    result = await session.execute(stmt)
    return result.scalars().first()

async def create_usuario(db: AsyncSession, usuario: crear_usuario):
    # Crear cliente en Stripe
    try:
        stripe_customer = stripe.Customer.create(
            name=usuario.nombre_usuario,
            email=usuario.correo_usuario
        )
        
        # Hash de la contraseña
        hashed_password = pwd_context.hash(usuario.password_usuario)
        
        # Crear usuario en la base de datos
        db_usuario = Usuario(
            nombre_usuario=usuario.nombre_usuario,
            correo_usuario=usuario.correo_usuario,
            telefono_usuario=usuario.telefono_usuario,
            password_usuario=hashed_password,
            rol_usuario=usuario.rol_usuario,
            region_usuario=usuario.region_usuario,
            stripe_customer_id=stripe_customer.id  # Guardar el ID del cliente de Stripe
        )
        
        db.add(db_usuario)
        await db.commit()
        await db.refresh(db_usuario)
        return db_usuario
        
    except stripe.error.StripeError as e:
        # Si hay un error con Stripe, hacer rollback de la transacción
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating Stripe customer: {str(e)}")
    except Exception as e:
        await db.rollback()
        raise e