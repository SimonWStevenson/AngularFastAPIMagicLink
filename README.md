# AngularFastAPIMagicLink

The purpose of this project is as a simple demo of Angular + FastAPI + magic link authentication.

Don't rely on any of this, I am not a developer

## Get link
- User enters email address
- System generates a magic link send it to the user in an email

## Validate link
- User opens their email and clicks the link
- System validates the user token from the URL parameter
+ must exist
+ must not be expired
+ must not have been used previously (it does this by setting to null on success)
- System generates a session token and saves it to a cookie

## Authenticate
- Angular site has an interceptor which sets withCredentials: true.  This means the cookie is sent with every request.
- FastAPI receives the session token from the cookie, decodes it, and uses it
- FastAPI returns 401 error if necessary
- Angular site has an interceptor which detects 401 errors and routes accordingly

## Notes
- Simple list of notes
- Unique logged in users have their own lists
- Purpose is to demo that separate user data has worked