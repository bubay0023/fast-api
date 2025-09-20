# FastAPI + SQLite Example

This is a simple FastAPI project using SQLite as the database. Includes Docker and docker-compose setup.

## Usage

### Local
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

API Endpoints:
- POST /items/ (name: str)
- GET /items/
