build:
	docker-compose build app

web/build:
	npm install
	npm run build

serve:
	docker-compose run -p 8000:8000 -v $(PWD):/app app
	docker-compose down

.PHONY: build serve web/build
