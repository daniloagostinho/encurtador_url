from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import shortuuid
from fastapi.responses import RedirectResponse

from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal, init_db, URL

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
def encurtar_url(request: URLRequest, db: Session = Depends(get_db)):
    short_code = shortuuid.ShortUUID().random(length=6)
    new_url = URL(short_code=short_code, original_url=str(request.url))
    db.add(new_url)
    db.commit()
    return {"short_url": f"http://127.0.0.1:8000/{short_code}"}

@app.get("/{short_code}")
def redirecionar_url(short_code: str, db: Session = Depends(get_db)):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()
    if url_entry:
        return RedirectResponse(url=url_entry.original_url)
    raise HTTPException(status_code=404, detail="URL encurtada não encontrada")