from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import shortuuid

from fastapi.responses import RedirectResponse

app = FastAPI()

# Simulando um banco de dados em memória
url_db = {}

class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

@app.get("/")
def read_root():
    return {"message": "API de Encurtador de URL está rodando!!!!!"}

@app.post("/encurtar", response_model=URLResponse)
def encurtar_url(request: URLRequest):
    # Gerar um código único curto
    short_code = shortuuid.ShortUUID().random(length=6)

    # Armazenar no "banco de dados" em memória
    url_db[short_code] = request.url

    # Retornar a URL encurtada (simulando um domínio fictício)
    return {"short_url": f"http://127.0.0.1:8000/{short_code}"}

@app.get("/{short_code}")
def redirecionar_url(short_code: str):
    # Verificar se o código curto existe no banco de dados em memória
    if short_code in url_db:
        url_original = url_db[short_code]
        return RedirectResponse(url=url_original)
    
    # Se não encontrar, retorna erro 404
    raise HTTPException(status_code=404, detail="URL encurtada não encontrada")