# poke-cards-global
Track Pokémon card releases, from the Japanese set -> English set

## scraping assets

```shell
./scripts/scraper.py https://jp.pokellector.com/VMAX-Climax-Expansion
./scripts/db_insert.py S8B
make build serve

# then visit http://localhost:8000/cards/
```


## DB

big thanks to this guide for the kick-start: https://fastapi.tiangolo.com/tutorial/sql-databases/
