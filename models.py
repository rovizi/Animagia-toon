from sqlalchemy import Column, Integer, String
from database import Base

class DesenhoItem(Base):
    __tablename__ = "desenhos_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    season_info = Column(String)           # Ex: 'Temporadas 1-7'
    age_rating = Column(String, default="Livre")
    cover_url = Column(String)
    playlist_url = Column(String)
    description = Column(String)