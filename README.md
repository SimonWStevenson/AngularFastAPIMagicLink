# AngularFastAPIMagicLink

The purpose of this project is as a simple demo of Angular + FastAPI + magic link authentication.

Don't rely on any of this, I am not a developer

## Key features
- Email link authentication.  User enters email address, system generates a magic link sends it to the user in an email, user clicks the link and it logs them in.
- Cookie is saved on the browser with a JWT that can be used to authenticate the user.
- Angular interceptor which sends the cookie to the API
- Angular interceptor which reads HTTP exceptions from the API and routes to /login if needed
- Angular guards which send user to /home if they are already logged in as per the cookie; or /login otherwise
- Session list which shows all sessions for this user
- Notes list, user can add notes.  Purpose is to demo filtering data by user.

## Setup

### FastAPI

Create a .env file in /api.
- Email settings are for outlook.com.  Enter email address and password in the .env.
- Choose your own JWT key.
- Set timeouts as appropriate.

~~~
ADMIN_EMAIL=""
ADMIN_PASSWORD=""
WEBSITE_URL="http://localhost:8085"
WEBSITE_URL_SERVE="http://localhost:4200"
SERVER_URL="http://localhost:8086"
JWT_SECRET_KEY=""
SESSION_TOKEN_DAYS=250
USER_TOKEN_MINUTES=30
~~~

### Angular

Angular code's API services currently have the URL to the API hardcoded to http://localhost:8086.

Angular container's nginx.conf currently has the server as localhost.