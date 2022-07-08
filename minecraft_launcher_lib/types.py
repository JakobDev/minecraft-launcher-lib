from typing import Optional, TypedDict, List, Callable
from enum import Enum
import datetime


class MinecraftOptions(TypedDict, total=False):
    username: str
    uuid: str
    token: str
    executablePath: str
    jvmArguments: List[str]
    launcherName: str
    launcherVersion: str
    gameDirectory: str
    demo: bool
    customResolution: bool
    resolutionWidth: str
    resolutionHeight: str
    server: str
    port: str
    nativesDirectory: str
    enableLoggingConfig: bool


class CallbackDict(TypedDict, total=False):
    setStatus: Callable[[str], None]
    setProgress: Callable[[int], None]
    setMax: Callable[[int], None]


class LatestMinecraftVersions(TypedDict):
    release: str
    snapshot: str


class MinecraftVersionInfo(TypedDict):
    id: str
    type: str
    releaseTime: datetime.datetime


class FabricMinecraftVersion(TypedDict):
    version: str
    stable: bool


class FabricLoader(TypedDict):
    separator: str
    build: int
    maven: str
    version: str
    stable: bool


# ----
# News
# ----


class ArticleLang(Enum):
    en_us = "en-us"


class BackgroundColor(Enum):
    bg_blue = "bg-blue"
    bg_green = "bg-green"
    bg_red = "bg-red"


class ContentType(Enum):
    image = "image"
    outgoing_link = "outgoing-link"
    video = "video"


class Image(TypedDict):
    content_type: ContentType
    imageURL: str
    alt: Optional[str]
    videoURL: Optional[str]
    videoType: Optional[str]
    videoProvider: Optional[str]
    videoId: Optional[str]
    linkurl: Optional[str]
    background_color: Optional[BackgroundColor]


class TileSize(Enum):
    the1x1 = "1x1"
    the1x2 = "1x2"
    the2x1 = "2x1"
    the2x2 = "2x2"
    the4x2 = "4x2"


class Tile(TypedDict):
    sub_header: str
    image: Image
    tile_size: TileSize
    title: str


class Article(TypedDict):
    default_tile: Tile
    articleLang: ArticleLang
    primary_category: str
    categories: List[str]
    article_url: str
    publish_date: str
    tags: List[str]
    preferred_tile: Optional[Tile]


class Articles(TypedDict):
    article_grid: List[Article]
    article_count: int
