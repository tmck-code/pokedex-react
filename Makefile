build:
	docker-compose build app

serve:
	docker-compose run -p 8000:8000 -v $(PWD):/app app
	docker-compose down

.PHONY: build serve
