from typing import List, TypedDict
import requests
import datetime


class RequestsResponseCache(TypedDict):
    response: requests.models.Response
    datetime: datetime.datetime


class MavenMetadata(TypedDict):
    release: str
    latest: str
    versions: List[str]
