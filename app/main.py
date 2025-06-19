import os
import uvicorn
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine

from app.database import Base
from app.routers import auth

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up auth service...")

    # Initialize database connection
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
    Base.metadata.create_all(bind=engine)

    yield
    # Shutdown
    print("Shutting down auth service...")

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"service": "Auth Service", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
