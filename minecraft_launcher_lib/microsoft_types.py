# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
This module contains all Types for the :doc:`microsoft_account` module.
It has it's own module because of the many types needed that are not used somewhere else.
"""
from typing import Any, Literal, TypedDict


class AuthorizationTokenResponse(TypedDict):
    access_token: str
    token_type: Literal["Bearer"]
    expires_in: int
    scope: str
    refresh_token: str


class _Xui(TypedDict):
    uhs: str


class _DisplayClaims(TypedDict):
    xui: list[_Xui]


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
    items: list[_MinecraftStoreItem]
    signature: str
    keyId: str


class MinecraftAuthenticateResponse(TypedDict):
    username: str
    roles: list[Any]
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
    skins: list[_MinecraftProfileSkin]
    capes: list[_MinecraftProfileCape]
    error: str
    errorMessage: str


class CompleteLoginResponse(MinecraftProfileResponse):
    access_token: str
    refresh_token: str
