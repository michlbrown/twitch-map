from typing import List
from dotenv import load_dotenv
import os
import httpx
from authlib.integrations.httpx_client import OAuth2Client
from pydantic import BaseModel

load_dotenv()
token_endpoint = "https://id.twitch.tv/oauth2/token"


class Stream(BaseModel):
    user_id: str
    user_name: str
    game_id: str
    game_name: str
    language: str
    viewer_count: int


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
streams = []
language = "en"
response = get_streams(client, language=language, limit=100)
data = response.json()["data"]

for stream in data:
    streams.append(Stream(**stream))

# get next page because previous response does not always include 100 streams
cursor = response.json()["pagination"]["cursor"]
response = get_streams(client, language=language, limit=20, after=cursor)
data2 = response.json()["data"]
for stream in data2:
    streams.append(Stream(**stream))

# get final list of 100 streams
seen_ids = set()
unique_streams = []
for stream in streams:
    id = stream.user_id

    if id not in seen_ids:
        unique_streams.append(stream)
        seen_ids.add(id)

unique_streams = unique_streams[:100]

# Merge with already tracked streams

# For all tracked streams that are online, get viewers

# Save viewers to db
