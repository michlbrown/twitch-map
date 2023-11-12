from dotenv import load_dotenv
import os
import httpx
from authlib.integrations.httpx_client import OAuth2Client

load_dotenv()
token_endpoint = "https://id.twitch.tv/oauth2/token"


def get_streams(
    client: OAuth2Client, language: str = None, limit: int = 20, after: str = None
) -> httpx.Response:
    url = "https://api.twitch.tv/helix/streams"
    headers = {"Client-Id": os.getenv("client_id")}

    params = {}
    if language is not None:
        params["language"] = language
    if after is not None:
        params["after"] = after
    params["first"] = limit

    response = client.get(url, params=params, headers=headers)
    return response


client = OAuth2Client(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    token_endpoint_auth_method="client_secret_post",
)
client.fetch_token(token_endpoint)

# Get top 100 streams
response = get_streams(client, language="en", limit=100)
streams = response.json()["data"]

# Merge with already tracked streams

# For all tracked streams that are online, get viewers

# Save viewers to db
