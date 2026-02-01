# JDEnhancer Backend

Flask API for JD Enhancement and Interview Generation.

## Structure

- `app.py` – Application factory and Flask setup
- `application.py` – WSGI entry (e.g. for `gunicorn backend.application:application`)
- `config.py` – Configuration (development, testing, production)
- `models.py` – SQLAlchemy models
- `interview_routes.py` – API routes
- `jd_enhancement_service.py` – JD enhancement logic
- `interview_generation_service.py` – Interview generation logic
- `claude_client.py` – Claude API client
- `prompts.py` – Prompt templates

## Run from project root

**Development (root):**
```bash
python app.py
# or
python -m backend.app
```

**Production (root):**
```bash
gunicorn application:application
# Uses root application.py which imports backend.app
```

**Database connection test:**
```bash
python -m backend.test_db_connection
```

**Tests:**
```bash
pytest backend/ -v
pytest backend/ --cov=backend
```

## Run from backend folder

```bash
cd backend
pip install -r requirements.txt
python -c "from app import create_app; create_app('development').run(port=5000)"
# or for DB test:
python test_db_connection.py
pytest test_services.py -v
```

## Environment

Use a `.env` file in the project root (or set env vars). See `database_config_example.env` and root README.
