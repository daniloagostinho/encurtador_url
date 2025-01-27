from fastapi import FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, HttpUrl
import shortuuid
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, URL
from cache import redis_client
import os
from fastapi import Request
from config import API_KEY

app = FastAPI()

RATE_LIMIT = 5  # Número máximo de requisições permitidas
RATE_WINDOW = 60  # Tempo (em segundos) para resetar o limite


# Configurar segurança para API Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Criar as tabelas no banco ao iniciar
init_db()

class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validar_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Acesso não autorizado")
    
def check_rate_limit(request: Request):
        client_ip = request.client.host  # Identificar o usuário pelo IP
        key = f"rate_limit:{client_ip}"

        # Verificar o número de requisições no Redis
        requests = redis_client.get(key)

        if requests is None:
            redis_client.setex(key, RATE_WINDOW, 1)  # Criar chave com expiração
        
        else:
            requests = int(requests)
        if requests >= RATE_LIMIT:
            raise HTTPException(status_code=429, detail="Muitas requisições. Tente novamente mais tarde.")
        redis_client.incr(key)  # Incrementa contador

@app.post("/encurtar", response_model=URLResponse)
def encurtar_url(
    request: URLRequest,
    req: Request,
    db: Session = Depends(get_db),
    _: str = Depends(validar_api_key),  # Exige API Key
):
    check_rate_limit(req)  # Aplica Rate-Limiting

    short_code = shortuuid.ShortUUID().random(length=6)
    new_url = URL(short_code=short_code, original_url=str(request.url))
    db.add(new_url)
    db.commit()

    host = req.headers.get("X-Forwarded-Host", req.base_url.hostname)
    port = req.headers.get("X-Forwarded-Port", req.base_url.port or "8001")
    full_url = f"http://{host}:{port}/{short_code}"

    return {"short_url": full_url}


@app.get("/{short_code}")
def redirecionar_url(short_code: str, db: Session = Depends(get_db)):
    # Primeiro, verificar se a URL já está em cache no Redis
    url_original = redis_client.get(short_code)
    
    if url_original:
        print(f"Cache HIT: {short_code} -> {url_original}")
        return RedirectResponse(url=url_original)

    # Se não estiver no cache, buscar no banco de dados
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    if url_entry:
        # Armazena a URL encurtada no Redis para acessos futuros
        redis_client.set(short_code, url_entry.original_url)
        print(f"Cache MISS: {short_code} armazenado no Redis")
        return RedirectResponse(url=url_entry.original_url)

    # Se não encontrar, retorna erro 404
    raise HTTPException(status_code=404, detail="URL encurtada não encontrada")