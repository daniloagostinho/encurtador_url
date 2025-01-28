import os
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Pega o DATABASE_URL da variável de ambiente, usa 'localhost' quando rodando localmente
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://encurtador_user:password@localhost:5433/encurtador")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo da Tabela URL
class URL(Base):
    __tablename__ = "urls"
    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)

# Criar as tabelas no banco de dados
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
