# Main libs
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DB, settings
from database.connection import Settings

# Routes
from routes.users import user_router
from routes.events import event_router


# Routes
app = FastAPI()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


# DB
@app.on_event("startup")
async def start_app():
    await Settings().initialize_database()


# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
