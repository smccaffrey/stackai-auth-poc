service_name = auth

# Run service locally
.PHONY: server
server:
	poetry run uvicorn --reload auth.app:app --host 0.0.0.0 --port 9898

# Create a new alembic version
.PHONY: alembic-migration
alembic-migration:
	@echo "Migration Description: "; \
    read MIGRATION_DESC; \
	PYTHONPATH=. poetry run alembic revision --autogenerate -m "$$MIGRATION_DESC"

# Upgrades local db with any new migrations
.PHONY: db-up
db-up:
	poetry run alembic upgrade head

# Undo last alembic migration
.PHONY: db-down
db-down:
	poetry run alembic downgrade -1

