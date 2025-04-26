from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tortoise import Tortoise
from dto.author_dto import AuthorDTO
from security.auth import create_access_token, decode_access_token
from models_db.author import Author

author_router = APIRouter(
    prefix="/author",     # Prefixo para todas as rotas aqui
    tags=["Author"],     
)

# Rota consultando todos authores na base de dados
@author_router.get("/get_all_author")
async def get_all_author():
    authors = await Author.all()
    return authors

@author_router.get("/get_all_author2")
async def get_all_author():
    # Exemplo de execução de uma consulta SQL diretamente
    query = """
        SELECT * FROM author 
    """
    result = await Tortoise.get_connection("default").execute_query(query)
    
    for row in result:
        print(row)
    return result

# Rota consultando author na base de dados
@author_router.get("/get_author/{id}")
async def get_author(id: int):
    authors = await Author.filter(id=id).first()
    print(authors)
    return authors


# Rota salvando author no banco de dados
@author_router.post("/save_author")
async def save_author(dto: AuthorDTO):
    print(f'{dto.id} - {dto.name}')
    authors = await Author.create(
        name=dto.name
    )
    return authors.id

# Rota salvando author no banco de dados
@author_router.post("/update_author")
async def update_author(dto: AuthorDTO):
    print(f'{dto.id} - {dto.name}')
    authors = await Author.filter(id=dto.id).update(
        name=dto.name
    )
    return authors

# Rota deletando author no banco de dados
@author_router.post("/delete_author/{id}")
async def delete_author(id: int):
    print(f'{id}')
    authors = await Author.filter(id=id).delete()
    return authors


