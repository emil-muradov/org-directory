# Organization Directory

A directory of organizations with location-based search capabilities.


## Database Schema

```
┌───────────────────────────┐
│         buildings         │
├───────────────────────────┤
│ id          SERIAL     PK │
│ address     TEXT          │
│ coordinates GEOMETRY      │
│ created_at  TIMESTAMP     │
│ updated_at  TIMESTAMP     │
└─────────────┬─────────────┘
              │
              │ 1:*
              ▼
┌─────────────┴─────────────┐                 ┌─────────────────────────────┐
│        organizations      │                 │            phones           │
├───────────────────────────┤                 ├─────────────────────────────┤
│ id          SERIAL     PK │ 1:*             │ id              SERIAL   PK │
│ name        TEXT       UK ├────────────────►│ organization_id INTEGER  FK │
│ building_id INTEGER    FK │                 │ phone_number    TEXT        │
│ created_at  TIMESTAMP     │                 │ created_at      TIMESTAMP   │
│ updated_at  TIMESTAMP     │                 │ updated_at      TIMESTAMP   │
└─────────────┬─────────────┘                 └─────────────────────────────┘
              │
              │ *:*
              ▼
┌─────────────┴─────────────┐
│  organization_industries  │
├───────────────────────────┤
│ organization_id INT PK,FK │
│ industry_id     INT PK,FK │
│ created_at      TIMESTAMP │
└─────────────┬─────────────┘
              │
              │ *:1
              ▼
┌─────────────┴─────────────┐
│          industries       │◄───┐
├───────────────────────────┤    │
│ id         SERIAL      PK │    │ parent_id
│ parent_id  INTEGER     FK │────┘ (self-ref)
│ name       TEXT        UK │
│ created_at TIMESTAMP      │
│ updated_at TIMESTAMP      │
└───────────────────────────┘
```

## Setup

1. Make sure you have Docker installed and running.

2. Create `.env` file in the project root and copy variables from `.env.example`

3.  **Start services:**
    ```
    make dev_compose_up
    ```

4.  **Set up database:**
    
    ```
    make dev_setup_db
    ```

5.  **Access the application:**
    *   API: http://localhost:3001
    *   Docs: http://localhost:3001/docs
