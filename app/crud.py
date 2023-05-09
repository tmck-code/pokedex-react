from sqlalchemy.orm import Session

from . import models, schemas


def get_set(db: Session, set_id: int):
    return db.query(models.Set).filter(models.Set.id == set_id).first()


def get_set_by_email(db: Session, code: str):
    return db.query(models.Set).filter(models.Set.code == code).first()


def get_sets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Set).offset(skip).limit(limit).all()


def create_set(db: Session, set: schemas.SetCreate):
    db_set = models.Set(name=set.name, code=set.code, description=set.description)
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set


def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()


def create_set_card(db: Session, card: schemas.CardCreate, set_id: int):
    db_card = models.Card(**card.dict(), set_id=set_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
