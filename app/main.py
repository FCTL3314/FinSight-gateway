from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine

from app.config import get_settings
from app.database import Base
from app.routers import auth

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up auth service...")

    engine = create_engine(
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
    )
    Base.metadata.create_all(bind=engine)

    yield
    print("Shutting down auth service...")

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"service": "Auth Service", "status": "running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
