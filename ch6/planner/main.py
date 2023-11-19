import uvicorn
from fastapi import FastAPI

from routes.users import user_router
from routes.events import event_router
from database.connection import conn


# Routes
app = FastAPI()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


# DB
@app.on_event("startup")
def on_startup():
    conn()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
