from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/card_sets/", response_model=schemas.CardSet)
def create_set(set: schemas.CardSetCreate, db: Session = Depends(get_db)):
    db_set = crud.get_set_by_code(db, code=set.code)
    if db_set:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_card_set(db=db, set=set)


@app.get("/card_sets/", response_model=list[schemas.CardSet])
def read_card_sets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    card_sets = crud.get_card_sets(db, skip=skip, limit=limit)
    return card_sets


@app.get("/card_sets/{card_set_id}", response_model=schemas.CardSet)
def read_set(card_set_id: int, db: Session = Depends(get_db)):
    db_card_set = crud.get_card_set(db, card_set_id=card_set_id)
    if db_card_set is None:
        raise HTTPException(status_code=404, detail="CardSet not found")
    return db_card_set


@app.post("/card_sets/{card_set_id}/cards/", response_model=schemas.Card)
def create_card_for_set(card_set_id: int, card: schemas.CardCreate, db: Session = Depends(get_db)):
    return crud.create_card(db=db, card=card, card_set_id=card_set_id)


@app.get("/cards/", response_model=list[schemas.Card])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = crud.get_cards(db, skip=skip, limit=limit)
    return sorted(cards, key=lambda x: x.number_in_set)

