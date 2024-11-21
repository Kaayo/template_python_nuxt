from io import BytesIO
import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from dto.author_dto import AuthorDTO
from models_db.author import Author
from models_db.db import exit_database, init_database
from security.auth import create_access_token, decode_access_token
import asyncio
from contextlib import asynccontextmanager
from reportlab.pdfgen import canvas
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código a ser executado quando o aplicativo iniciar
    print("App iniciado!")
    
    print('Subindo database ...')
    await init_database()
    print('Database iniciado!')
    
    # Quando o aplicativo for fechado
    yield
    
    # Fechando a conexão com o banco de dados
    print('Encerrando database ...')
    await exit_database()
    print('Database encerrado!')
    
    # Código a ser executado quando o aplicativo for fechado
    print("App finalizado!")

app = FastAPI(lifespan=lifespan)

# Define the allowed origins
origins = [
    "*",  # Allow all origins
]

# Add CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins to allow
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# OAuth2PasswordBearer é uma classe que facilita a obtenção do token no cabeçalho da requisição
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Classe de usuário (para simulação)
class User(BaseModel):
    username: str

# Rota pública (sem JWT necessário)
@app.get("/")
async def read_root():
    asyncio.sleep(2)
    return {"message": "Bem-vindo à rota pública"}

# Rota para login, que retorna o JWT
@app.post("/token")
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
@app.get("/protected")
async def read_protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Olá {current_user.username}, você tem acesso a esta rota protegida!"}

# Outra rota protegida
@app.get("/profile")
async def read_profile(current_user: User = Depends(get_current_user)):
    return {"message": f"Perfil de {current_user.username}"}

# Rota consultando todos authores na base de dados
@app.get("/get_all_author")
async def get_all_author():
    authors = await Author.all()
    return authors

# Rota consultando author na base de dados
@app.get("/get_author/{id}")
async def get_author(id: int):
    authors = await Author.filter(id=id).first()
    print(authors)
    return authors


# Rota salvando author no banco de dados
@app.post("/save_author")
async def save_author(dto: AuthorDTO):
    print(f'{dto.id} - {dto.name}')
    authors = await Author.create(
        name=dto.name
    )
    return authors.id

# Rota salvando author no banco de dados
@app.post("/update_author")
async def update_author(dto: AuthorDTO):
    print(f'{dto.id} - {dto.name}')
    authors = await Author.filter(id=dto.id).update(
        name=dto.name
    )
    return authors

# Rota deletando author no banco de dados
@app.post("/delete_author/{id}")
async def delete_author(id: int):
    print(f'{id}')
    authors = await Author.filter(id=id).delete()
    return authors

@app.get("/generate-pdf")
async def generate_pdf():
    # Criar um buffer em memória para o PDF
    buffer = BytesIO()

    # Criar o PDF com ReportLab
    c = canvas.Canvas(buffer, pagesize=letter)  # 'letter' tem tamanho A4 em ReportLab (8.5 x 11 polegadas)
    
    # Adicionar conteúdo ao PDF
    c.drawString(100, 750, "Este é um exemplo de PDF gerado com FastAPI!")
    c.drawString(100, 735, "Ele está no formato A4 (tamanho carta no ReportLab).")
    
    # Salvar o PDF no buffer
    c.save()
    
    # Posicionar o buffer no início para leitura
    buffer.seek(0)

    # Retornar o PDF como resposta para o usuário
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=exemplo.pdf"})

## uvicorn main:app --reload
## python -m uvicorn main:app --reload --port 8080
