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
            cover_url="https://i.postimg.cc/GtK0SW7F/chaves-desenho.jpg",
            playlist_url="https://www.youtube.com/embed/PUmhmTNZFjE",
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
                display: flex;
                align-items: center;
                justify-content: center;
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
            .play-btn {{
                background-color: #ffcc00;
                border: none;
                width: 64px;
                height: 64px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                transition: transform 0.2s, background-color 0.2s;
                z-index: 2;
            }}
            .play-btn:hover {{
                transform: scale(1.1);
                background-color: #ffd633;
            }}
            .play-icon {{
                width: 32px;
                height: 32px;
                fill: #121212;
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
            /* Modal / Player na tela */
            .modal {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.9);
                justify-content: center;
                align-items: center;
                z-index: 100;
            }}
            .modal-content {{
                position: relative;
                width: 80%;
                max-width: 800px;
                aspect-ratio: 16/9;
            }}
            .modal-content iframe {{
                width: 100%;
                height: 100%;
                border: none;
                border-radius: 8px;
            }}
            .close-btn {{
                position: absolute;
                top: -40px;
                right: 0;
                color: white;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
                background: none;
                border: none;
            }}
        </style>
    </head>
    <body>
        <div class="header-title">Animagia Toon</div>
        <div class="card">
            <div class="card-header">
                <span class="badge-age">{desenho.age_rating}</span>
                <button class="play-btn" onclick="openPlayer()" title="Assistir">
                    <svg class="play-icon" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                    </svg>
                </button>
            </div>
            <div class="card-body">
                <h2 class="title">{desenho.title}</h2>
                <p class="description"><strong>{desenho.season_info}</strong> • {desenho.description}</p>
                <div class="sinopse-box">
                    <strong>Sinopse:</strong> {desenho.sinopse}
                </div>
            </div>
        </div>

        <!-- Player Modal -->
        <div id="videoModal" class="modal">
            <div class="modal-content">
                <button class="close-btn" onclick="closePlayer()">&times;</button>
                <iframe id="videoFrame" src="" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>
        </div>

        <script>
            function openPlayer() {{
                const modal = document.getElementById('videoModal');
                const iframe = document.getElementById('videoFrame');
                iframe.src = "{desenho.playlist_url}?autoplay=1";
                modal.style.display = "flex";
            }}

            function closePlayer() {{
                const modal = document.getElementById('videoModal');
                const iframe = document.getElementById('videoFrame');
                iframe.src = "";
                modal.style.display = "none";
            }}
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/desenhos/", response_model=list[schemas.Desenho])
def listar_desenhos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    desenhos = db.query(models.Desenho).offset(skip).limit(limit).all()
    return desenhos
