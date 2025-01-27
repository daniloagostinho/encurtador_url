from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, HttpUrl
import shortuuid
from fastapi.responses import RedirectResponse

from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal, init_db, URL

from cache import redis_client

app = FastAPI()

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

@app.post("/encurtar", response_model=URLResponse)
def encurtar_url(request: URLRequest, req: Request, db: Session = Depends(get_db)):
    # Gerar um código único curto
    short_code = shortuuid.ShortUUID().random(length=6)

    # Salvar no banco de dados
    new_url = URL(short_code=short_code, original_url=str(request.url))
    db.add(new_url)
    db.commit()

    # Detectar corretamente o host e a porta
    host = req.headers.get("X-Forwarded-Host", req.base_url.hostname)
    forwarded_port = req.headers.get("X-Forwarded-Port")

    # Usar a porta real exposta pelo NGINX (8001) se for acessado externamente
    port = forwarded_port if forwarded_port else req.base_url.port
    if not port or port in ["None", "80"]:
        port = 8001  # Porta externa usada no Docker

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