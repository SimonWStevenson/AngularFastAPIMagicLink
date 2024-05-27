from functools import lru_cache
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from . import database, security, config
engine = create_engine("sqlite:///db///MagicLink.db", echo=True, connect_args={"check_same_thread": False})

@lru_cache
def get_settings():
    return config.Settings()

app = FastAPI(debug=True)
myapi = FastAPI(debug=True)
settings = get_settings()

# CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.website_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.on_event("startup")
def on_startup():
    print("i wake up!")
    database.setupDatabase()
    database.initialiseData()
    return

@myapi.get("/open")
async def open():
    return {"message": "Hello World"}

@myapi.get("/users")
async def read_users_me(current_user: security.CurrentUser):
    return {"id": current_user.id, "email": current_user.email}

@myapi.post("/login/{email}")
def login(email: str):
    return security.login(email)

@myapi.get("/verify")
def verify(request: Request, user_token: str, email: str):
    redirect_response = security.verify(request=request, user_token=user_token, email=email)
    return redirect_response

@myapi.get("/authenticated")
async def authenticated(current_user: security.CurrentUser):
    return {"message": "You have logged in successfully"}

@myapi.get("/notes")
def get_notes(current_user: security.CurrentUser):
    return database.getNotes(current_user)

@myapi.post("/note")
def add_note(note, current_user: security.CurrentUser):
    return database.addNote(note, current_user)

app.mount ("/api", myapi)