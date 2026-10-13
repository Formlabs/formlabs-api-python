"""AsyncFormlabsSession and its blocking twin: one login, both token families, automatic renewal."""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Callable

import httpx

from .._sync import SyncOwner, adopt
from .errors import (
    FormlabsAuthError,
    InvalidCredentialsError,
    MissingCredentialsError,
    TokenRefreshError,
)
from .store import InMemoryTokenStore, TokenStore
from .tokens import DeveloperToken, TokenKind, UserToken, decode_jwt_exp, redact

DEFAULT_BASE_URL = "https://api.formlabs.com"
USER_TOKEN_PATH = "/o/token/"
USER_REFRESH_PATH = "/o/token/refresh/"
DEVELOPER_TOKEN_PATH = "/developer/v1/o/token/"
DEVELOPER_REVOKE_PATH = "/developer/v1/o/revoke_token/"

# Refresh/re-mint a token this many seconds before its wall-clock expiry.
DEFAULT_REFRESH_SKEW = 300.0

_DASHBOARD_HINT = (
    "client_id and client_secret come from https://dashboard.formlabs.com/#developer"
)


@dataclass
class FormlabsCredentials:
    """Credentials for the two token families.

    - ``username``/``password`` mint the **user token**, accepted by PreForm
      API ``/v1/login/``.
    - ``client_id``/``client_secret`` alone mint the **developer token**
      (OAuth2 client credentials).

    Provide only the pairs you need; a token is minted lazily on first request
    and a missing pair raises :class:`MissingCredentialsError` at that point.
    """

    username: str | None = None
    password: str | None = None
    client_id: str | None = None
    client_secret: str | None = None

    def __repr__(self) -> str:
        return (
            f"FormlabsCredentials(username={self.username!r}, "
            f"password={'***' if self.password else None}, "
            f"client_id={self.client_id!r}, "
            f"client_secret={'***' if self.client_secret else None})"
        )


def _server_detail(response: httpx.Response) -> str:
    """Extract the server's error payload verbatim (never contains tokens)."""
    try:
        data = response.json()
    except ValueError:
        return response.text[:500]
    if isinstance(data, dict) and ("error" in data or "error_description" in data):
        return "; ".join(
            str(data[key]) for key in ("error", "error_description") if key in data
        )
    return json.dumps(data)


class AsyncFormlabsSession:
    """Holds, refreshes, and routes both Formlabs token families.

    Log in once with :class:`FormlabsCredentials`; call :meth:`user_token` or
    :meth:`developer_token` whenever a request needs one. Tokens are minted
    lazily, refreshed proactively (``refresh_skew`` seconds before expiry),
    and concurrent callers share a single in-flight mint/refresh per family.

    Closing the session (``async with`` exit or :meth:`aclose`) revokes the
    developer token best-effort and clears all local token state. The user
    token cannot be revoked; it stays valid until it expires, about 90 days
    after it was minted. Treat a leaked user token accordingly.
    """

    def __init__(
        self,
        credentials: FormlabsCredentials,
        *,
        base_url: str = DEFAULT_BASE_URL,
        store: TokenStore | None = None,
        http_client: httpx.AsyncClient | None = None,
        refresh_skew: float = DEFAULT_REFRESH_SKEW,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._credentials = credentials
        self._base_url = base_url.rstrip("/")
        self._store: TokenStore = store if store is not None else InMemoryTokenStore()
        self._owns_client = http_client is None
        self._client = http_client if http_client is not None else httpx.AsyncClient()
        self._refresh_skew = refresh_skew
        self._clock = clock
        self._locks = {
            TokenKind.USER: asyncio.Lock(),
            TokenKind.DEVELOPER: asyncio.Lock(),
        }

    @property
    def http_client(self) -> httpx.AsyncClient:
        """The HTTP client this session uses; shared with the client's children."""
        return self._client

    async def __aenter__(self) -> "AsyncFormlabsSession":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def user_token(self) -> str:
        """Return a valid user (SimpleJWT) access token, minting or refreshing as needed."""
        token = self._store.load(TokenKind.USER)
        if isinstance(token, UserToken) and not token.expires_within(
            self._refresh_skew, now=self._clock()
        ):
            return token.access
        async with self._locks[TokenKind.USER]:
            # A concurrent caller may have minted or refreshed while we
            # waited for the lock.
            token = self._store.load(TokenKind.USER)
            if isinstance(token, UserToken):
                if not token.expires_within(self._refresh_skew, now=self._clock()):
                    return token.access
                token = await self._refresh_user_token(token)
            else:
                token = await self._mint_user_token()
            self._store.save(TokenKind.USER, token)
            return token.access

    async def developer_token(self) -> str:
        """Return a valid developer (OAuth2) access token, re-requesting as needed.

        This family has no refresh token; near expiry a fresh token is minted.
        """
        token = self._store.load(TokenKind.DEVELOPER)
        if isinstance(token, DeveloperToken) and not token.expires_within(
            self._refresh_skew, now=self._clock()
        ):
            return token.access_token
        async with self._locks[TokenKind.DEVELOPER]:
            token = self._store.load(TokenKind.DEVELOPER)
            if isinstance(token, DeveloperToken) and not token.expires_within(
                self._refresh_skew, now=self._clock()
            ):
                return token.access_token
            token = await self._mint_developer_token()
            self._store.save(TokenKind.DEVELOPER, token)
            return token.access_token

    def invalidate(self, kind: TokenKind) -> None:
        """Drop the cached token of ``kind`` so the next call re-mints it.

        Call this when a request comes back 401 despite a token the session
        thought was valid.
        """
        self._store.clear(TokenKind(kind))

    async def aclose(self) -> None:
        """Revoke the developer token (best effort) and clear all local token state.

        The user token cannot be revoked; only the session's local copy is
        discarded, and the token stays valid until it expires.
        """
        token = self._store.load(TokenKind.DEVELOPER)
        if (
            isinstance(token, DeveloperToken)
            and self._credentials.client_id
            and self._credentials.client_secret
        ):
            try:
                await self._client.post(
                    self._base_url + DEVELOPER_REVOKE_PATH,
                    data={
                        "token": token.access_token,
                        "client_id": self._credentials.client_id,
                        "client_secret": self._credentials.client_secret,
                    },
                )
            except httpx.HTTPError:
                pass  # best effort: the token self-expires within 24h anyway
        self._store.clear(TokenKind.USER)
        self._store.clear(TokenKind.DEVELOPER)
        if self._owns_client:
            await self._client.aclose()

    async def _mint_user_token(self) -> UserToken:
        creds = self._credentials
        if not (creds.username and creds.password):
            raise MissingCredentialsError(
                "username/password are required to mint a user token "
                "(needed for any call that signs in with the account)"
            )
        url = self._base_url + USER_TOKEN_PATH
        # This is a Django SimpleJWT login view, not an OAuth token endpoint:
        # no grant_type; the response has `access`, alias `access_token`, and
        # `refresh`, but no `expires_in`. Secrets may contain `+ & = %`, so the
        # body must be form-encoded (httpx's `data=` does this).
        response = await self._client.post(
            url,
            data={"username": creds.username, "password": creds.password},
        )
        if response.status_code != 200:
            raise InvalidCredentialsError(
                f"user token request failed with HTTP {response.status_code}",
                endpoint=url,
                detail=_server_detail(response),
            )
        payload = response.json()
        access = payload.get("access") or payload.get("access_token")
        refresh = payload.get("refresh")
        if not access or not refresh:
            raise FormlabsAuthError(
                "user token response missing 'access'/'refresh' fields",
                endpoint=url,
            )
        return UserToken(
            access=access, refresh=refresh, expires_at=decode_jwt_exp(access)
        )

    async def _refresh_user_token(self, token: UserToken) -> UserToken:
        url = self._base_url + USER_REFRESH_PATH
        # JSON body, not form-encoded; the refresh token is not rotated.
        response = await self._client.post(url, json={"refresh": token.refresh})
        if response.status_code != 200:
            raise TokenRefreshError(
                f"user token refresh failed with HTTP {response.status_code}",
                endpoint=url,
                detail=_server_detail(response),
            )
        payload = response.json()
        access = payload.get("access") or payload.get("access_token")
        if not access:
            raise TokenRefreshError(
                "user token refresh response missing 'access' field", endpoint=url
            )
        # Keep the old refresh token unless the server unexpectedly rotates it.
        return UserToken(
            access=access,
            refresh=payload.get("refresh") or token.refresh,
            expires_at=decode_jwt_exp(access),
        )

    async def _mint_developer_token(self) -> DeveloperToken:
        creds = self._credentials
        if not (creds.client_id and creds.client_secret):
            raise MissingCredentialsError(
                f"client_id/client_secret are required to mint a developer token; {_DASHBOARD_HINT}"
            )
        url = self._base_url + DEVELOPER_TOKEN_PATH
        minted_at = self._clock()
        response = await self._client.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
            },
        )
        if response.status_code != 200:
            raise InvalidCredentialsError(
                f"developer token request failed with HTTP {response.status_code}",
                endpoint=url,
                detail=_server_detail(response),
            )
        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise FormlabsAuthError(
                "developer token response missing 'access_token' field", endpoint=url
            )
        return DeveloperToken(
            access_token=access_token,
            expires_at=minted_at + float(payload.get("expires_in", 86400)),
            token_type=payload.get("token_type", "Bearer"),
            scope=payload.get("scope", ""),
        )

    def __repr__(self) -> str:
        return (
            f"AsyncFormlabsSession(base_url={self._base_url!r}, "
            f"credentials={self._credentials!r})"
        )


class FormlabsSession(SyncOwner):
    """Blocking twin of :class:`AsyncFormlabsSession`; ``client.auth`` on ``FormlabsClient``.

    Same constructor and methods, called without ``await``. A session built
    standalone runs on its own event-loop thread; a client or child given it
    as ``session=`` runs on that thread too and leaves the session open.
    """

    def __init__(
        self,
        credentials: FormlabsCredentials,
        *,
        base_url: str = DEFAULT_BASE_URL,
        store: TokenStore | None = None,
        http_client: httpx.AsyncClient | None = None,
        refresh_skew: float = DEFAULT_REFRESH_SKEW,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._attach(
            AsyncFormlabsSession(
                credentials,
                base_url=base_url,
                store=store,
                http_client=http_client,
                refresh_skew=refresh_skew,
                clock=clock,
            ),
            None,
        )

    def user_token(self) -> str:
        """A valid user access token, minting or refreshing as needed."""
        return self._run(self._async.user_token())

    def developer_token(self) -> str:
        """A valid developer access token, re-requesting as needed."""
        return self._run(self._async.developer_token())

    def invalidate(self, kind: TokenKind) -> None:
        """Drop the cached token of ``kind`` so the next call re-mints it."""
        self._async.invalidate(kind)


__all__ = [
    "AsyncFormlabsSession",
    "FormlabsCredentials",
    "FormlabsSession",
    "DEFAULT_BASE_URL",
    "DEFAULT_REFRESH_SKEW",
]
