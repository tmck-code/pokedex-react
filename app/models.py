from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    items = relationship("Image", back_populates="owner")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    code = Column(String, index=True)
    image_url = Column(String, index=False)
    description = Column(String, index=True)
    set_id = Column(Integer, ForeignKey("sets.id"))

    owner = relationship("Set", back_populates="cards")
