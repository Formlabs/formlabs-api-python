"""Formlabs SDK.

:class:`FormlabsClient` holds the account and exposes each API as a child:
``client.auth`` (:class:`FormlabsSession`) and ``client.preform``
(:class:`PreFormApi`, over the generated PreForm API v1 client
``formlabs_preform_api``).
:class:`AsyncFormlabsClient` and the ``Async``-prefixed classes are the same
surface with ``await``.
"""

from .auth import (
    AsyncFormlabsSession,
    DEFAULT_BASE_URL,
    DEFAULT_REFRESH_SKEW,
    DeveloperToken,
    FormlabsAuthError,
    FormlabsCredentials,
    FormlabsSession,
    InMemoryTokenStore,
    InvalidCredentialsError,
    MissingCredentialsError,
    TokenKind,
    TokenRefreshError,
    TokenStore,
    UserToken,
)
from .client import AsyncFormlabsClient, FormlabsClient
from .errors import FormlabsError
from .preform_api import AsyncPreFormApi, PreFormApi, PreFormApiError

__all__ = [
    "AsyncFormlabsClient",
    "FormlabsClient",
    "FormlabsError",
    "AsyncPreFormApi",
    "PreFormApi",
    "PreFormApiError",
    "DEFAULT_BASE_URL",
    "DEFAULT_REFRESH_SKEW",
    "DeveloperToken",
    "FormlabsAuthError",
    "FormlabsCredentials",
    "AsyncFormlabsSession",
    "FormlabsSession",
    "InMemoryTokenStore",
    "InvalidCredentialsError",
    "MissingCredentialsError",
    "TokenKind",
    "TokenRefreshError",
    "TokenStore",
    "UserToken",
]

__version__ = "1.0.0-alpha"
