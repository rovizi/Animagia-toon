from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Animagia Desenhos API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def seed_data():
    db = next(get_db())
    if db.query(models.DesenhoItem).count() == 0:
        initial_item = models.DesenhoItem(
            title="Chaves em Desenho",
            season_info="Temporadas 1-7",
            age_rating="Livre",
            cover_url="https://i.postimg.cc/MTtdkzwX/chaves-desenho.jpg",
            playlist_url="https://www.youtube.com/watch?v=pUmhmTNZFiE&list=PL-rGbptKz8EXcQpBnH6LzLk03BZO5FowS",
            description="As aventuras completas da vizinhança em versão animada (Temporadas 1 a 7)."
        )
        db.add(initial_item)
        db.commit()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API exclusiva de Desenhos do Animagia!"}

@app.get("/desenhos/", response_model=list[schemas.DesenhoResponse])
def get_desenhos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.DesenhoItem).offset(skip).limit(limit).all()
    return items

@app.post("/desenhos/", response_model=schemas.DesenhoResponse)
def create_desenho(item: schemas.DesenhoCreate, db: Session = Depends(get_db)):
    db_item = models.DesenhoItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item