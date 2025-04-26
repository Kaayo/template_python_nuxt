from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from dto.author_dto import AuthorDTO
from security.auth import create_access_token, decode_access_token

auth_router = APIRouter(
    prefix="/auth",     # Prefixo para todas as rotas aqui
    tags=["Auth"],      #
)

# OAuth2PasswordBearer é uma classe que facilita a obtenção do token no cabeçalho da requisição
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Classe de usuário (para simulação)
class User(BaseModel):
    username: str

# Rota para login, que retorna o JWT
@auth_router.post("/token")
async def login_for_access_token(form_data: dict):
    # Em uma aplicação real, você verificaria as credenciais no banco de dados
    # Para simplificar, vamos simular uma verificação de usuário
    if form_data['username'] == "admin" and form_data['password'] == "secret":
        access_token = create_access_token(data={"sub": form_data['username']})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

# Dependência para obter o usuário atual a partir do JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(username=payload["sub"])

# Rota protegida: exige JWT válido
@auth_router.get("/protected")
async def read_protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Olá {current_user.username}, você tem acesso a esta rota protegida!"}

# Outra rota protegida
@auth_router.get("/profile")
async def read_profile(current_user: User = Depends(get_current_user)):
    return {"message": f"Perfil de {current_user.username}"}

