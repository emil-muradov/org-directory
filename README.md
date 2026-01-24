# Organization Directory

A directory of organizations with location-based search capabilities.


## Database Schema

```
┌───────────────────────────┐
│         Building          │
├───────────────────────────┤
│ id          SERIAL     PK │
│ address     STRING        │
│ coordinates GEOMETRY      │
│ created_at  DATETIME      │
│ updated_at  DATETIME      │
└─────────────┬─────────────┘
              │
              │ 1:*
              ▼
┌─────────────┴─────────────┐                 ┌─────────────────────────────┐
│        Organization       │                 │            Phone            │
├───────────────────────────┤                 ├─────────────────────────────┤
│ id          SERIAL     PK │ 1:*             │ id              SERIAL   PK │
│ name        STRING     UK ├────────────────►│ organization_id INTEGER  FK │
│ building_id INTEGER    FK │                 │ phone_number    STRING      │
│ created_at  DATETIME      │                 │ created_at      DATETIME    │
│ updated_at  DATETIME      │                 │ updated_at      DATETIME    │
└─────────────┬─────────────┘                 └─────────────────────────────┘
              │
              │ *:*
              ▼
┌─────────────┴─────────────┐
│  organization_industries  │
├───────────────────────────┤
│ organization_id INT PK,FK │
│ industry_id     INT PK,FK │
│ created_at      DATETIME  │
└─────────────┬─────────────┘
              │
              │ *:1
              ▼
┌─────────────┴─────────────┐
│          Industry         │◄───┐
├───────────────────────────┤    │
│ id         SERIAL      PK │    │ parent_id
│ parent_id  INTEGER     FK │────┘ (self-ref)
│ name       STRING      UK │
│ created_at DATETIME       │
│ updated_at DATETIME       │
└───────────────────────────┘
```

## Setup

### Option 1: Using Docker (Recommended)

1. Create `.env` file in the project root and copy variables from `.env.example`

2.  **Start services:**
    ```bash
    docker compose up --watch
    ```

3.  **Set up database:**
    
    Wait for the database to be ready, then run the following commands to set up extensions and schema.

    ```bash
    # Enable required extensions
    docker compose exec db psql -U org -d postgres -c "create extension if not exists postgis;"
    docker compose exec db psql -U org -d postgres -c "create extension if not exists pg_trgm;"
    docker compose exec db psql -U org -d postgres -c "create extension if not exists btree_gin;"

    # Run migrations
    docker compose exec app alembic upgrade head

    # (Optional) Seed test data
    cat scripts/seed_test_data.sql | docker compose exec -T db psql -U org -d postgres
    ```

4.  **Access the application:**
    *   API: http://localhost:3001
    *   Docs: http://localhost:3001/docs

### Option 2: Local Setup (Without Docker)

**Prerequisites:**
*   Python 3.13+
*   PostgreSQL with PostGIS installed locally (or use docker image `postgis/postgis:15-3.4-alpine`)

1. **Create virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install .
    # Install dev dependencies if needed
    pip install ".[dev,test]"
    ```

3.  **Configure environment:**
    Create a `.env` file (or use environment variables) with your database connection:
    ```bash
    DB_URL=postgresql+asyncpg://org:org@db:5432/postgres
    ```

4.  **Set up database:**
    Make sure your local Postgres database exists and has extensions enabled:
    ```bash
    psql -U org -d postgres -c "create extension if not exists postgis;"
    psql -U org -d postgres -c "create extension if not exists pg_trgm;"
    psql -U org -d postgres -c "create extension if not exists btree_gin;"
    ```

5.  **Run migrations:**
    ```bash
    alembic upgrade head
    ```

6.  **Run the app:**
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 3001 --reload
    ```
