dev_compose_up:
	docker compose -f compose.dev.yml up --build --watch

dev_compose_down:
	docker compose -f compose.dev.yml down --volumes

dev_setup_db:
	docker compose -f compose.dev.yml exec db psql -U org -d postgres -c "create extension if not exists postgis;"
	docker compose -f compose.dev.yml exec db psql -U org -d postgres -c "create extension if not exists pg_trgm;"
	docker compose -f compose.dev.yml exec db psql -U org -d postgres -c "create extension if not exists btree_gin;"
	docker compose -f compose.dev.yml exec app alembic -c src/infrastructure/persistence/db/alembic/alembic.ini upgrade head
	cat src/infrastructure/persistence/db/seed_test_data.sql | docker compose -f compose.dev.yml exec -T db psql -U org -d postgres

dev_alembic_run:
	docker compose -f compose.dev.yml exec app alembic -c src/infrastructure/persistence/db/alembic/alembic.ini upgrade head

dev_alembic_reset:
	docker compose -f compose.dev.yml exec app alembic -c src/infrastructure/persistence/db/alembic/alembic.ini stamp base

dev_alembic_add_migration:
	docker compose -f compose.dev.yml exec app alembic -c src/infrastructure/persistence/db/alembic/alembic.ini revision --autogenerate -m "$(message)"
	