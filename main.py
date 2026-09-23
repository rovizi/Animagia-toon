from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Animagia Toon API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    # Verifica se já existe o registro para evitar duplicação
    existing = db.query(models.Desenho).first()
    if not existing:
        novo_desenho = models.Desenho(
            title="Chaves em Desenho",
            season_info="Temporadas 1-7",
            age_rating="Livre",
            cover_url="https://i.postimg.com/MTtdkzwX/chaves-desenho.jpg",
            playlist_url="https://www.youtube.com/watch?v=PUmhmTNZFjE&list=PL-rGbptKz8EXcQpBnH6LzLk03BZ05FowS",
            description="As aventuras completas da vizinhança em versão animada (Temporadas 1 a 7).",
            sinopse="A clássica turma da vizinhança ganha vida nesta versão animada repleta de diversão e confusões. Acompanhe Chaves, Chiquinha, Kiko e todos os moradores em episódios inéditos e releituras das melhores histórias que marcaram gerações, agora em formato de animação para toda a família."
        )
        db.add(novo_desenho)
        db.commit()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API exclusiva de Desenhos do Animagia!"}

@app.get("/desenhos/", response_model=list[schemas.Desenho])
def listar_desenhos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    desenhos = db.query(models.Desenho).offset(skip).limit(limit).all()
    return desenhos