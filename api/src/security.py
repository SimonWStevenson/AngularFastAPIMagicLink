from datetime import datetime, timedelta
from functools import lru_cache
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from user_agents import parse
import jwt
from . import database, config, emails

@lru_cache
def get_settings():
    return config.Settings()

class UserSession:
    def __init__(self, user_id: int, session_id: int, email: str):
        self.user_id = user_id
        self.session_id = session_id
        self.email = email

# Generate magic link and email it
def login(email: str, settings):
    my_user = database.getUser(email)
    if not my_user:
        my_user = database.createUser(email)
    user_token = jwt.encode(
        {
            "email": email, 
            "exp": datetime.now() + timedelta(minutes=settings.user_token_minutes)
        }, 
        settings.jwt_secret_key, 
        algorithm="HS256"
    )
    database.setUserToken(email, user_token)
    emails.send_magic_link(email, user_token, settings)
    return {"An email with a login link has been sent to " +  email}

# Verify user token and supply session token
def verify(request: Request, user_token: str, email: str, settings):
    user_agent = request.headers.get("user-agent")
    device_info = get_device_info(user_agent)
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
            my_session = database.setSessionToken(user_id=my_user.id, device_info=device_info)
            session_token = jwt.encode(
                {
                    "email": email,
                    "session_id": my_session.id,
                    "exp": datetime.now() + timedelta(days=settings.session_token_days),
                }, 
                settings.jwt_secret_key, 
                algorithm="HS256"
            )
            redirect_response = RedirectResponse(url=settings.website_url + "/home")
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
def get_user(request: Request, settings: Annotated[config.Settings, Depends(get_settings)]) -> UserSession:
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

    my_email = decoded_session_token['email']
    my_session_id = decoded_session_token['session_id']
    my_user_session = database.getSessionToken(email=my_email, session_id=my_session_id)
    if my_user_session:
        my_user_result = UserSession(user_id=my_user_session.user_id, session_id=my_user_session.id, email=my_email)
        return my_user_result
    else:
        print("Session token user not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

CurrentUser = Annotated[UserSession, Depends(get_user)]

def is_logged_in(request: Request, settings: Annotated[config.Settings, Depends(get_settings)]) -> bool:
    session_token = request.cookies.get("session_token")
    if not session_token:
        return False

    try:
        decoded_session_token = jwt.decode(session_token, settings.jwt_secret_key, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False

    my_email = decoded_session_token['email']
    my_session_id = decoded_session_token['session_id']
    my_user_session = database.getSessionToken(email=my_email, session_id=my_session_id)
    return bool(my_user_session)



def get_device_info(user_agent: str) -> str:
    user_agent_parsed = parse(user_agent)
    device_info = {
        "browser": user_agent_parsed.browser.family,
        "browser_version": user_agent_parsed.browser.version_string,
        "os": user_agent_parsed.os.family,
        "os_version": user_agent_parsed.os.version_string,
        "device": user_agent_parsed.device.family,
        "device_brand": user_agent_parsed.device.brand,
        "device_model": user_agent_parsed.device.model,
        "is_mobile": user_agent_parsed.is_mobile,
        "is_tablet": user_agent_parsed.is_tablet,
        "is_pc": user_agent_parsed.is_pc,
        "is_bot": user_agent_parsed.is_bot,
    }
    return device_info