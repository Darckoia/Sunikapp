# SUNIKFLOW

Plataforma web musical basada en FastAPI + frontend estático, inspirada funcionalmente en herramientas tipo Suno pero con identidad visual diferenciada.

## Desarrollo

```bash
pip install -r backend/requirements.txt
cd backend
uvicorn main:app --reload
```

Frontend y API quedan servidos en `http://localhost:8000`.

## Tests

```bash
pytest backend/tests -q
```
