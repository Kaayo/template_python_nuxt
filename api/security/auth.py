import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = "minhachavesecreta"  # Alterar para uma chave mais segura
ALGORITHM = "HS256"  # Algoritmo HMAC
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Tempo de expiração do token

# Função para criar o token JWT
def create_access_token(data: dict, expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) + timedelta(minutes=expires_in) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para decodificar o token JWT e obter os dados do usuário
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload if payload["exp"] >= datetime.now(timezone.utc).timestamp() else None
    except jwt.PyJWTError:
        return None
