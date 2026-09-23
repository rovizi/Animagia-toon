from sqlalchemy import Column, Integer, String
from database import Base

class Desenho(Base):
    __tablename__ = "desenhos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    season_info = Column(String)
    age_rating = Column(String)
    cover_url = Column(String)
    playlist_url = Column(String)
    description = Column(String)
    sinopse = Column(String, nullable=True)  # Novo campo de sinopse