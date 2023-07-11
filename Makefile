build:
	docker-compose build app

web/build:
	npm install
	npm run build

web/serve:
	npm start

docker/serve:
	docker-compose run -p 8000:8000 -v $(PWD):/app app

poc/files:
	./scripts/scraper.py 'https://jp.pokellector.com/Pokemon-151-Expansion/' 'cards'
	./scripts/scraper.py 'https://jp.pokellector.com/Violet-ex-Expansion/' 'cards'
	./scripts/scraper.py 'https://jp.pokellector.com/Snow-Hazard-Expansion/' 'cards'
	./scripts/db_insert.py 'cards'
	cp -R ./cards ./src/

poc/docker: poc/files web/build docker/serve web/serve


.PHONY: build web/serve docker/serve web/build poc/docker poc/files
