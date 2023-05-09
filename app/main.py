from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sets/", response_model=schemas.Set)
def create_set(set: schemas.SetCreate, db: Session = Depends(get_db)):
    db_set = crud.get_set_by_email(db, email=set.email)
    if db_set:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_set(db=db, set=set)


@app.get("/sets/", response_model=list[schemas.Set])
def read_sets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sets = crud.get_sets(db, skip=skip, limit=limit)
    return sets


@app.get("/sets/{set_id}", response_model=schemas.Set)
def read_set(set_id: int, db: Session = Depends(get_db)):
    db_set = crud.get_set(db, set_id=set_id)
    if db_set is None:
        raise HTTPException(status_code=404, detail="Set not found")
    return db_set


@app.post("/sets/{set_id}/cards/", response_model=schemas.Card)
def create_card_for_set(set_id: int, card: schemas.CardCreate, db: Session = Depends(get_db)):
    return crud.create_set_card(db=db, card=card, set_id=set_id)


@app.get("/cards/", response_model=list[schemas.Card])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = crud.get_cards(db, skip=skip, limit=limit)
    return cards
