from sqlalchemy.orm import Session

from . import models, schemas


def get_set(db: Session, card_set_id: int):
    return db.query(models.CardSet).filter(models.CardSet.id == card_set_id).first()


def get_card_set_by_code(db: Session, code: str):
    return db.query(models.CardSet).filter(models.CardSet.code == code).first()


def get_card_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CardSet).offset(skip).limit(limit).all()


def create_card_set(db: Session, card_set: schemas.CardSetCreate):
    db_card_set = models.CardSet(name=card_set.name, code=card_set.code, description=card_set.description)
    db.add(db_card_set)
    db.commit()
    db.refresh(db_card_set)
    return db_card_set


def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()


def create_card(db: Session, card: schemas.CardCreate, card_set_id: int):
    db_card = models.Card(**card.dict(), card_set_id=card_set_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
