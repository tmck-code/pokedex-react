from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class CardSet(Base):
    __tablename__ = "card_sets"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    cards = relationship("Card", back_populates="card_set")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    number_in_set = Column(Integer, index=True)
    title = Column(String, index=True)
    image_url = Column(String, index=False)
    description = Column(String, index=True)
    card_set_id = Column(Integer, ForeignKey("card_sets.id"))

    card_set = relationship("CardSet", back_populates="cards")
