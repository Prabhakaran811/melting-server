
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.database import (
    SessionLocal,
    check_database_connection,
)
from app.api.router import api_router
from app.services.admin_seed_service import ensure_initial_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()

    try:
        ensure_initial_admin(db)
        yield
    finally:
        db.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/health/database")
def database_health():
    try:
        check_database_connection()
        return {
            "status": "connected",
            "database": "PostgreSQL",
        }
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )


app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)
