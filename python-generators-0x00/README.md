# Python Generators - Task 0 (PostgreSQL via Docker Compose)

This script connects to a PostgreSQL database running in Docker, creates a `user_data` table, and populates it from a CSV file.

## Setup Instructions

1. Start the PostgreSQL container:
```bash
docker-compose up -d
```

2. Install Python requirements:
```bash
pip install psycopg2-binary
```

3. Run the seeding script:
```bash
chmod +x 0-main.py
./0-main.py
```

## Notes
- The PostgreSQL container runs with:
  - Hostname: `db`
  - Port: `5432`
  - User: `postgres`
  - Password: `postgres`
  - Default DB: `postgres`