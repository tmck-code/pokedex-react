build:
	docker-compose build app

web/build:
	npm install
	npm run build

serve:
	docker-compose run -p 8000:8000 -v $(PWD):/app -d app
	npm start

poc_files:
	./scripts/scraper.py 'https://jp.pokellector.com/VMAX-Climax-Expansion/'
	./scripts/db_insert.py S8B
	cp -Rv ./S8B ./src/

poc: poc_files web/build serve


.PHONY: build serve web/build poc poc_files
