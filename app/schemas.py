from pydantic import BaseModel


class CardBase(BaseModel):
    number_in_set: int
    title: str
    image_url: str
    description: str | None = None


class CardCreate(CardBase): pass

class Card(CardBase):
    card_set_code: str

    class Config:
        orm_mode = True


class CardSetBase(BaseModel):
    code: str
    name: str
    description: str | None = None


class CardSetCreate(CardSetBase): pass


class CardSet(CardSetBase):
    Cards: list[Card] = []

    class Config:
        orm_mode = True

