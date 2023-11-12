from dotenv import load_dotenv
import os
import httpx
from authlib.integrations.httpx_client import OAuth2Client

load_dotenv()
token_endpoint = "https://id.twitch.tv/oauth2/token"


def get_streams(
    client: OAuth2Client, after: str = "", language: str = "en", limit: int = 20
) -> httpx.Response:
    url = "https://api.twitch.tv/helix/streams"
    headers = {"Client-Id": os.getenv("client_id")}
    params = {"language": language, "first": limit, "after": after}
    response = client.get(url, params=params, headers=headers)

    return response


client = OAuth2Client(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    token_endpoint_auth_method="client_secret_post",
)
client.fetch_token(token_endpoint)

streams = get_streams(client, limit=100).json()["data"]
print(streams)
