from typing import Literal, TypedDict, List, Callable
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


class _ImageBase(TypedDict):
    content_type: Literal["image", "outgoing-link", "video"]
    imageURL: str


class Image(_ImageBase, total=False):
    alt: str
    videoURL: str
    videoType: str
    videoProvider: str
    videoId: str
    linkurl: str
    background_color: Literal["bg-blue", "bg-green", "bg-red"]


class Tile(TypedDict):
    sub_header: str
    image: Image
    tile_size: Literal["1x1", "1x2", "2x1", "2x2", "4x2"]
    title: str


class _ArticleBase(TypedDict):
    default_tile: Tile
    articleLang: Literal["en-us"]
    primary_category: str
    categories: List[str]
    article_url: str
    publish_date: str
    tags: List[str]


class Article(_ArticleBase, total=False):
    preferred_tile: Tile


class Articles(TypedDict):
    article_grid: List[Article]
    article_count: int
