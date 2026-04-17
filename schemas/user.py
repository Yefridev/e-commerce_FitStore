from pydantic import BaseModel, EmailStr

# Modelo para crear usuario
class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

# Modelo para login de usuario
class UserLogin(BaseModel):
    email: str
    password: str

# Modelo para respuesta de usuario
class userResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr