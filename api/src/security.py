from datetime import datetime, timedelta
from functools import lru_cache
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
import jwt
from . import database, config, emails

@lru_cache
def get_settings():
    return config.Settings()

class User:
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email

# Generate magic link and email it
def login(email: str):
    settings = get_settings()
    my_user = database.getUser(email)
    if not my_user:
        my_user = database.createUser(email)
    user_token = jwt.encode(
        {"email": email, "exp": datetime.now() + timedelta(minutes=settings.user_token_minutes)}, 
        settings.jwt_secret_key, 
        algorithm="HS256"
    )
    database.setUserToken(email, user_token)
    emails.send_magic_link(email, user_token, settings)
    return {"An email with a login link has been sent to " +  email}


# Verify user token and supply session token
def verify(user_token: str, email: str):
    settings = get_settings()
    try:
        decoded_user_token = jwt.decode(user_token, settings.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("User token has expired")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except jwt.InvalidTokenError:
        print("User token is invalid")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    decoded_user_token_email = decoded_user_token['email']
    if email == decoded_user_token_email:
        my_user = database.getUser(email)
        if not my_user:
            print("User token user not found")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        elif my_user['user_token'] != user_token:
            print("User token is invalid for this user")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        elif my_user['user_token'] == user_token:
            print("Valid user token")
            database.expireUserToken(email)
            session_token = jwt.encode({"email": email}, settings.jwt_secret_key, algorithm="HS256")
            database.setSessionToken(email, session_token)
            redirect_response = RedirectResponse(url=settings.website_url + "/authenticated")
            redirect_response.set_cookie(
                key="session_token", 
                value=session_token, 
                max_age=settings.session_token_days * 24 * 60 * 60, # max_age is measured in seconds
                httponly=True,
                secure=True,
                samesite='none'
            )
            return redirect_response
        else:
            print("User token unauthorized - unknown error")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        print("User token is invalid")
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Authenticate every request
def get_user(request: Request, settings: Annotated[config.Settings, Depends(get_settings)]) -> User:
    session_token = request.cookies.get("session_token")
    if not session_token:
        print("Session token not found in browser")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        decoded_session_token = jwt.decode(session_token, settings.jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print("Session token has expired")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except jwt.InvalidTokenError:
        print("Session token is invalid")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    decoded_session_token_email = decoded_session_token['email']

    my_user = database.getUser(decoded_session_token_email)
    my_user_result = User(id=my_user.id, email=my_user.email)
    if not my_user:
        print("Session token user not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    elif my_user and my_user['session_token'] == session_token:
        return my_user_result
    elif my_user['session_token'] != session_token:
        print("Session token is invalid for this user")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        print("Session token unauthorized - unknown error")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
CurrentUser = Annotated[User, Depends(get_user)]
