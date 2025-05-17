from fastapi import FastAPI
from app.routes import router
from app.db import init_db

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Notification Service is running"}
