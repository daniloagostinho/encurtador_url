from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import shortuuid

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
