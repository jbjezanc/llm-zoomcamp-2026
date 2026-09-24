

make run:
	uv run python assistant.py

chat:
	uv run streamlit run app.py

dashboard:
	uv run streamlit run dashboard.py

grafana-up:
	docker compose -f docker-compose.grafana.yml up -d

grafana-down:
	docker compose -f docker-compose.grafana.yml up -d

grafana-down:
	docker compose -f docker-compose.grafana.yml down

grafana-destroy:
	docker compose -f docker-compose.grafana.yml down -v

network:
	docker network create monitoring

postgres: network
	docker run -it \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5432:5432 \
		-v pgdata:/var/lib/postgresql/data \
		postgres:17


query:
	uv run python db_query.py