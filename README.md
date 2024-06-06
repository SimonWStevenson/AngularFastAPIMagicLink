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