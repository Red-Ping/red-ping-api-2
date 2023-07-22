from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status

from .db import crud, models, schemas
from .db.database import SessionLocal, engine
from .auth.access import router as access_router
from .ping.request import router as ping_request_router

from .auth.access import setup_secret_key
from . import config




app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(access_router)
app.include_router(ping_request_router)


@lru_cache()
def get_settings():
    return config.Settings()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = next(get_db())

setup_secret_key(get_settings().secret_key)
@app.get("/info")
@app.get("/")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

#Sends a ping to a user
@app.post("/ping_send")
def post_ping_send():
    return {"status": "healthy"}

#Get the current pings
@app.get("/ping_send")
def get_ping_send():
    return {"status": "healthy"}
