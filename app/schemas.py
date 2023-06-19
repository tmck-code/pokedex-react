from pydantic import BaseModel


class CardBase(BaseModel):
    number_in_set: int
    title: str
    image_url: str
    description: str | None = None


class CardCreate(CardBase): pass

class Card(CardBase):
    id: int
    card_set_id: int

    class Config:
        orm_mode = True


class CardSetBase(BaseModel):
    code: str
    name: str
    description: str | None = None


class CardSetCreate(CardSetBase): pass


class CardSet(CardSetBase):
    id: int
    Cards: list[Card] = []

    class Config:
        orm_mode = True

