import json
from typing import Mapping

import google.auth.transport.requests as req
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from google.auth import jwt
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

app = FastAPI()
GOOGLE_SCOPE = ["https://www.googleapis.com/auth/userinfo.email", "openid"]

flow = Flow.from_client_secrets_file(client_secrets_file="client_secret.json", scopes=GOOGLE_SCOPE)
flow.redirect_uri = "http://localhost:8000/login"


def get_client_info_from_json():
    with open("client_secret.json") as json_file:
        data = json.load(json_file)
        res = {"client_id": data["web"]["client_id"], "client_secret": data["web"]["client_secret"]}
    return res


CLIENT_INFO = get_client_info_from_json()


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

    return credentials._id_token


@app.get("/auth")
async def redirect() -> RedirectResponse:
    url = flow.authorization_url(
        access_type="offline",
    )[0]
    return RedirectResponse(url)


@app.post("/update_token")
async def update_access_token(refresh_token) -> dict[str, str]:
    """
    TODO: 1. add checking if refresh token in db and it's valid
    """
    info = CLIENT_INFO.copy()
    info.update({"refresh_token": refresh_token})
    creds = Credentials.from_authorized_user_info(info=info, scopes=GOOGLE_SCOPE)
    request = req.Request()
    creds.refresh(request)
    return creds
