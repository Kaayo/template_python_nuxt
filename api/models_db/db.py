# main.py

import asyncio
from tortoise import Tortoise
from models_db import Author, Todo  # Agora você pode importar diretamente

async def init_database():
    # Configuração do banco de dados PostgreSQL
    await Tortoise.init(
        db_url='postgres://postgres:postgres@localhost:5432/python_api',  # Insira suas credenciais
        modules={'models_db': ['models_db.author', 'models_db.todo']}
    )

async def exit_database():
    await Tortoise.close_connections()

#     # Geração das tabelas
#     await Tortoise.generate_schemas()

#     # Criando um autor
#     author = await Author.create(name="J.K. Rowling")

#     # Criando alguns todos para o autor
#     await Todo.create(description="Write a new book", author=author)
#     await Todo.create(description="Check deadlines", author=author)

#     # Consultando todos os todos de um autor
#     todos = await author.todos.all()
#     for todo in todos:
#         print(f"Todo: {todo.description}, Completed: {todo.completed}")

# # Rodando a função de inicialização
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init())
