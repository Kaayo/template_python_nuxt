from fastapi import FastAPI
from contextlib import asynccontextmanager
from models_db.db import exit_database, init_database

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