from pydantic import BaseModel


class CardBase(BaseModel):
    title: str
    image_url: str
    description: str | None = None


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int
    set_id: int

    class Config:
        orm_mode = True


class SetBase(BaseModel):
    name: str
    code: str
    description: str | None = None


class SetCreate(SetBase):
    pass


class Set(SetBase):
    id: int
    Cards: list[Card] = []

    class Config:
        orm_mode = True

