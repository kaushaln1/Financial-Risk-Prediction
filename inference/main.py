from fastapi import FastAPI
from app.api import user_router
from app.core.config import settings
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title=settings.PROJECT_NAME)

# Instrument Prometheus metrics
Instrumentator().instrument(app).expose(app)

app.include_router(user_router.router, prefix="/api/v1", tags=["users"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
