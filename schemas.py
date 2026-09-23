from pydantic import BaseModel

class DesenhoBase(BaseModel):
    title: str
    season_info: str
    age_rating: str = "Livre"
    cover_url: str
    playlist_url: str
    description: str

class DesenhoCreate(DesenhoBase):
    pass

class DesenhoResponse(DesenhoBase):
    id: int

    class Config:
        from_attributes = True