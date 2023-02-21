"""
This module contains all Types for the :doc:`microsoft_account` module.
It has it's own module because of the many types needed that are not used somewhere else.
"""
from typing import Any, Literal, TypedDict, List


class AuthorizationTokenResponse(TypedDict):
    access_token: str
    token_type: Literal["Bearer"]
    expires_in: int
    scope: str
    refresh_token: str


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
    roles: List[Any]
    access_token: str
    token_type: str
    expires_in: int


class _MinecraftProfileInfo(TypedDict):
    id: str
    state: Literal["ACTIVE", "INACTIVE"]
    url: str


class _MinecraftProfileSkin(_MinecraftProfileInfo):
    variant: str


class _MinecraftProfileCape(_MinecraftProfileInfo):
    alias: str


class MinecraftProfileResponse(TypedDict):
    id: str
    name: str
    skins: List[_MinecraftProfileSkin]
    capes: List[_MinecraftProfileCape]


class CompleteLoginResponse(MinecraftProfileResponse):
    access_token: str
    refresh_token: str
