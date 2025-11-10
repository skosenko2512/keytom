up:
	docker compose up -d --build
migrate:
	docker compose exec web python manage.py migrate
subs:
	docker compose exec web python manage.py runsubscribers
test:
	docker compose exec web pytest -q --cov
