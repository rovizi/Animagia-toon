from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Animagia Toon API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    db = next(get_db())
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

@app.get("/", response_class=HTMLResponse)
def read_root(db: Session = Depends(get_db)):
    desenho = db.query(models.Desenho).first()
    
    if not desenho:
        return "<h1>Nenhum desenho cadastrado.</h1>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Animagia - {desenho.title}</title>
        <style>
            body {{
                background-color: #121212;
                color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
            }}
            .header-title {{
                font-size: 22px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 16px;
                letter-spacing: 1px;
                text-transform: uppercase;
            }}
            .card {{
                background-color: #1e1e1e;
                border-radius: 16px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.6);
                width: 320px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                border: 1px solid #2a2a2a;
            }}
            .card-header {{
                position: relative;
                width: 100%;
                height: 400px;
                background-image: url('{desenho.cover_url}');
                background-size: cover;
                background-position: center;
            }}
            .badge-age {{
                position: absolute;
                top: 12px;
                right: 12px;
                background-color: #00c853;
                color: #ffffff;
                padding: 4px 10px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 6px;
            }}
            .card-body {{
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }}
            .title {{
                font-size: 18px;
                font-weight: bold;
                margin: 0;
                color: #ffffff;
            }}
            .description {{
                font-size: 13px;
                color: #b0b0b0;
                margin: 0;
                line-height: 1.4;
            }}
            .sinopse-box {{
                font-size: 12px;
                color: #dcdcdc;
                background-color: #252525;
                padding: 10px;
                border-radius: 8px;
                margin-top: 4px;
                line-height: 1.4;
            }}
            .btn {{
                display: block;
                text-align: center;
                background-color: #e50914;
                color: white;
                text-decoration: none;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 12px;
                transition: background 0.2s;
            }}
            .btn:hover {{
                background-color: #f40612;
            }}
        </style>
    </head>
    <body>
        <div class="header-title">Animagia Toon</div>
        <div class="card">
            <div class="card-header">
                <span class="badge-age">{desenho.age_rating}</span>
            </div>
            <div class="card-body">
                <h2 class="title">{desenho.title}</h2>
                <p class="description"><strong>{desenho.season_info}</strong> • {desenho.description}</p>
                <div class="sinopse-box">
                    <strong>Sinopse:</strong> {desenho.sinopse}
                </div>
                <a href="{desenho.playlist_url}" target="_blank" class="btn">Assistir Maratona</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/desenhos/", response_model=list[schemas.Desenho])
def listar_desenhos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    desenhos = db.query(models.Desenho).offset(skip).limit(limit).all()
    return desenhos
