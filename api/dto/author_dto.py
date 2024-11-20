# Definindo um DTO com Pydantic
from pydantic import BaseModel


class AuthorDTO(BaseModel):
    id: int
    name: str