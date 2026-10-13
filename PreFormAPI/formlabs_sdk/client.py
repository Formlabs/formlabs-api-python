"""The clients: one object holding the account and the API children."""

from __future__ import annotations

from typing import Any

import httpx

from ._sync import SyncOwner, adopt
from .auth import (
    DEFAULT_BASE_URL,
    DEFAULT_REFRESH_SKEW,
    AsyncFormlabsSession,
    FormlabsCredentials,
    FormlabsSession,
    TokenStore,
)
from .preform_api import AsyncPreFormApi, PreFormApi


class AsyncFormlabsClient:
    """Entry point to the Formlabs APIs.

    ``client.auth`` is the :class:`AsyncFormlabsSession` that mints and refreshes
    tokens; ``client.preform`` (:class:`AsyncPreFormApi`) drives a
    PreFormServer once launched or connected. Each child draws its credentials
    from ``client.auth``.

    Credentials are optional: without them an unauthenticated PreFormServer
    still works, and anything that needs the account raises
    ``MissingCredentialsError``. Pass ``session=`` to share an existing
    session; the client then leaves it open on close.

    Construction does no I/O. Close with ``async with`` or ``aclose()``: an
    SDK-launched PreFormServer is terminated, then an owned session is closed.
    """

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        credentials: FormlabsCredentials | None = None,
        session: AsyncFormlabsSession | None = None,
        api_base_url: str = DEFAULT_BASE_URL,
        http_client: httpx.AsyncClient | None = None,
        store: TokenStore | None = None,
        refresh_skew: float = DEFAULT_REFRESH_SKEW,
    ) -> None:
        if credentials is not None and (username is not None or password is not None):
            raise TypeError("pass credentials= or username= and password=, not both")
        if session is not None:
            given = [
                name
                for name, value in (
                    ("username", username),
                    ("password", password),
                    ("credentials", credentials),
                    ("store", store),
                )
                if value is not None
            ]
            if refresh_skew != DEFAULT_REFRESH_SKEW:
                given.append("refresh_skew")
            if given:
                raise TypeError(
                    "session= already carries credentials and token settings; "
                    f"drop {', '.join(given)}"
                )
            self.auth = session
            self._owns_session = False
        else:
            if credentials is None:
                credentials = FormlabsCredentials(username=username, password=password)
            self.auth = AsyncFormlabsSession(
                credentials,
                base_url=api_base_url,
                store=store,
                http_client=http_client,
                refresh_skew=refresh_skew,
            )
            self._owns_session = True

        self.preform = AsyncPreFormApi(session=self.auth)

    @property
    def owns_session(self) -> bool:
        """``False`` when the session was passed in; the client then never closes it."""
        return self._owns_session

    async def aclose(self) -> None:
        """Close each child, then an owned session.

        Each step runs even if an earlier one raises; the first exception
        propagates.
        """
        steps = [
            self.preform.aclose,
        ]
        if self._owns_session:
            steps.append(self.auth.aclose)
        error: BaseException | None = None
        for step in steps:
            try:
                await step()
            except BaseException as exc:
                if error is None:
                    error = exc
        if error is not None:
            raise error

    async def __aenter__(self) -> "AsyncFormlabsClient":
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.aclose()


class FormlabsClient(SyncOwner):
    """Blocking twin of :class:`AsyncFormlabsClient`.

    Same constructor; ``client.auth`` and ``client.preform`` are the blocking
    :class:`FormlabsSession` and :class:`PreFormApi`. The async implementation
    runs on a private event-loop thread that ``close()`` (or leaving the
    ``with`` block) stops. Pass a blocking ``FormlabsSession`` as ``session=``
    to share one; the client then runs on that session's thread and leaves the
    session open.
    """

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        credentials: FormlabsCredentials | None = None,
        session: FormlabsSession | AsyncFormlabsSession | None = None,
        api_base_url: str = DEFAULT_BASE_URL,
        http_client: httpx.AsyncClient | None = None,
        store: TokenStore | None = None,
        refresh_skew: float = DEFAULT_REFRESH_SKEW,
    ) -> None:
        async_session, loop = adopt(session)
        self._attach(
            AsyncFormlabsClient(
                username=username,
                password=password,
                credentials=credentials,
                session=async_session,
                api_base_url=api_base_url,
                http_client=http_client,
                store=store,
                refresh_skew=refresh_skew,
            ),
            loop,
        )
        runner = self._runner
        self.auth = (
            session if isinstance(session, FormlabsSession) else FormlabsSession._wrap(self._async.auth, runner)
        )
        self.preform = PreFormApi._wrap(self._async.preform, runner)

    @property
    def owns_session(self) -> bool:
        return self._async.owns_session
