from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI, Request
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

########################################################################
# APIs - security
########################################################################

@myapi.get("/login")
async def is_logged_in(request: Request):
    return security.is_logged_in(request=request, settings=settings)

@myapi.post("/login/{email}")
def login(email: str, settings: Annotated[config.Settings, Depends(get_settings)]):
    return security.login(email, settings)

@myapi.get("/session")
async def get_sessions(current_user: security.CurrentUser):
    return database.getSessions(current_user.user_id, current_user.session_id)

@myapi.delete("/session")
def delete_session(session_id: int, current_user: security.CurrentUser):
    return database.deleteSession(user_id=current_user.user_id, session_id=session_id)

@myapi.get("/verify")
def verify(request: Request, user_token: str, email: str, settings: Annotated[config.Settings, Depends(get_settings)]):
    redirect_response = security.verify(request=request, user_token=user_token, email=email, settings=settings)
    return redirect_response

########################################################################
# APIs - list of notes
########################################################################

@myapi.get("/notes")
def get_notes(current_user: security.CurrentUser):
    return database.getNotes(current_user)

@myapi.post("/notes")
def add_note(note, current_user: security.CurrentUser):
    return database.addNote(note, current_user)

########################################################################
# Finish
########################################################################

app.mount ("/api", myapi)