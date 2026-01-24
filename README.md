# Organization Directory

A directory of organizations with location-based search capabilities.

## Setup

### Option 1: Using Docker (Recommended)

1.  **Start the services:**
    ```bash
    docker compose up --watch
    ```

2.  **Initialize the Database:**
    
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

3.  **Access the application:**
    *   API: http://localhost:3001
    *   Docs: http://localhost:3001/docs

### Option 2: Local Setup (Without Docker)

**Prerequisites:**
*   Python 3.13+
*   PostgreSQL with PostGIS installed locally

1.  **Install dependencies:**
    ```bash
    pip install .
    # Install dev dependencies if needed
    pip install ".[dev,test]"
    ```

2.  **Configure Environment:**
    Create a `.env` file (or use environment variables) with your database connection:
    ```bash
    DB_URL=postgresql+asyncpg://org:org@db:5432/postgres
    ```

3.  **Setup Database:**
    Make sure your local Postgres database exists and has extensions enabled:
    ```bash
    psql -U org -d postgres -c "create extension if not exists postgis;"
    psql -U org -d postgres -c "create extension if not exists pg_trgm;"
    psql -U org -d postgres -c "create extension if not exists btree_gin;"
    ```

4.  **Run Migrations:**
    ```bash
    alembic upgrade head
    ```

5.  **Run the App:**
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 3001 --reload
    ```
