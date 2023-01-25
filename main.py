from google.auth import jwt
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from typing import Mapping

app = FastAPI()
GOOGLE_SCOPE = ["openid", "https://www.googleapis.com/auth/userinfo.email"]

flow = Flow.from_client_secrets_file(client_secrets_file="client_secret.json", scopes=GOOGLE_SCOPE)
flow.redirect_uri = "http://localhost:8000/login"


@app.get("/login")
async def exchange_authcode(code: str) -> Mapping[str, str]:
    """
    Exchanges authorization code for access token

    1) Frontend sends info with clientID, redirectURI and scope.
    2) The user logs in and grants permission to the app
    3) OAuth2 redirects user to specified redirectURI along with an AUTHORIZATION CODE

    4) frontend sends AUTHORIZATION CODE  to the backend
    5) Backend sends POST-request to google along with app_info and auth_code.
    6) Google responds with an access token and refresh token
    7) Access token to authenticate user
    8) post request to exchange the refresh token for access token
    """
    flow.fetch_token(code=code)
    credentials = flow.credentials
    user_info = jwt.decode(credentials._id_token, verify=False)

    return user_info


@app.get("/auth")
async def redirect() -> RedirectResponse:
    url = flow.authorization_url()[0]
    return RedirectResponse(url)
