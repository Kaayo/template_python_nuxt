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
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from fastapi.responses import FileResponse
from reportlab.platypus import Image
from endpoints.auth import auth_router
from endpoints.author import author_router
from endpoints.pdf import pdf_router
from hooks_api.lifespan import lifespan

## uvicorn main:app --reload
## python -m uvicorn main:app --reload --port 8080

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

# Incluindo os endpoints do módulo 'pdf'
app.include_router(auth_router)
app.include_router(author_router)
app.include_router(pdf_router)

# Rota pública (sem JWT necessário)
@app.get("/")
async def read_root():
    asyncio.sleep(2)
    return {"message": "Bem-vindo à rota pública!!!"}

