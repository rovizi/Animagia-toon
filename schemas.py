from pydantic import BaseModel
from typing import Optional

class DesenhoBase(BaseModel):
    title: str
    season_info: str
    age_rating: str
    cover_url: str
    playlist_url: str
    description: str
    sinopse: Optional[str] = None  # Incluído no schema

class DesenhoCreate(DesenhoBase):
    pass

class Desenho(DesenhoBase):
    id: int

    class Config:
        orm_mode = True

