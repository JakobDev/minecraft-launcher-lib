from typing import TypedDict, List


class AuthorizationTokenResponse(TypedDict):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str
    user_id: str
    foci: str


class _Xui(TypedDict):
    uhs: str


class _DisplayClaims(TypedDict):
    xui: List[_Xui]


class XBLResponse(TypedDict):
    IssueInstant: str
    NotAfter: str
    Token: str
    DisplayClaims: _DisplayClaims


class XSTSResponse(TypedDict):
    IssueInstant: str
    NotAfter: str
    Token: str
    DisplayClaimns: _DisplayClaims


class _MinecraftStoreItem(TypedDict):
    name: str
    signature: str


class MinecraftStoreResponse(TypedDict):
    items: List[_MinecraftStoreItem]
    signature: str
    keyId: str


class MinecraftAuthenticateResponse(TypedDict):
    username: str
    roles: List
    access_token: str
    token_type: str
    expires_in: int


class _MinecraftProfileSkin(TypedDict):
    id: str
    state: str
    url: str
    variant: str
    alias: str


class MinecraftProfileResponse(TypedDict):
    id: str
    name: str
    skins: List[_MinecraftProfileSkin]
    capes: List


class CompleteLoginResponse(MinecraftProfileResponse):
    access_token: str
    refresh_token: str
