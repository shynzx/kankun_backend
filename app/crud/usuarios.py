from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import UsuarioCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.correo_usuario == email).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
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
    db.commit()
    db.refresh(db_usuario)
    return db_usuario