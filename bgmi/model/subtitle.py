from pydantic import BaseModel


class Subtitle(BaseModel):
    id: str
    name: str
