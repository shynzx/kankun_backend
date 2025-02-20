from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.usuarios import Usuario
from app.schemas.usuarios import crear_usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_usuario_by_email(session: AsyncSession, correo_usuario: str):
    stmt = select(Usuario).where(Usuario.correo_usuario == correo_usuario)  # Filtro correcto
    result = await session.execute(stmt)  # Ejecutar consulta
    return result.scalars().first()  # Obtener el primer resultado

async def create_usuario(db: AsyncSession, usuario: crear_usuario):
    hashed_password = pwd_context.hash(usuario.password_usuario)
    db_usuario = Usuario(
        nombre_usuario=usuario.nombre_usuario,
        correo_usuario=usuario.correo_usuario,
        telefono_usuario=usuario.telefono_usuario,
        password_usuario=hashed_password,
        rol_usuario=usuario.rol_usuario,
        region_usuario=usuario.region_usuario
    )
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)  # Recargar para ver los ultimos cambios
    return db_usuario