"""Token dataclasses and JWT expiry decoding.

Two independent token families exist behind api.formlabs.com:

- **User token** (SimpleJWT): minted at ``POST /o/token/``, ~90-day JWT,
  refreshed via ``POST /o/token/refresh/``. Accepted by PreForm API
  ``/v1/login/``.
- **Developer token** (OAuth2 client_credentials): minted at
  ``POST /developer/v1/o/token/``, opaque, 24-hour lifetime, no refresh
  token.
"""

from __future__ import annotations

import base64
import binascii
import json
import time
from dataclasses import dataclass
from enum import Enum


def redact(secret: str) -> str:
    """Render a secret safely for logs and ``repr``: first 8 chars + length."""
    return f"{secret[:8]}...[{len(secret)} chars]"


class TokenKind(str, Enum):
    USER = "user"
    DEVELOPER = "developer"


def decode_jwt_exp(token: str) -> float:
    """Read the ``exp`` claim from a JWT payload without verifying the signature.

    The ``/o/token/`` response carries no ``expires_in``, so wall-clock expiry
    must be read from the JWT itself. No server-side introspection exists.
    """
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return float(payload["exp"])
    except (IndexError, KeyError, TypeError, ValueError, binascii.Error) as exc:
        raise ValueError(
            f"could not decode 'exp' claim from JWT {redact(token)}"
        ) from exc


@dataclass
class UserToken:
    """SimpleJWT access/refresh pair from ``POST /o/token/``.

    The refresh token is not rotated on refresh; ``expires_at`` comes from the
    access JWT's ``exp`` claim.
    """

    access: str
    refresh: str
    expires_at: float  # unix epoch seconds

    def expires_within(self, seconds: float, *, now: float | None = None) -> bool:
        return (now if now is not None else time.time()) >= self.expires_at - seconds

    def __repr__(self) -> str:
        return (
            f"UserToken(access={redact(self.access)}, "
            f"refresh={redact(self.refresh)}, expires_at={self.expires_at})"
        )


@dataclass
class DeveloperToken:
    """Opaque OAuth2 token from ``POST /developer/v1/o/token/``.

    There is no refresh token for this family; a new token is re-requested
    when this one nears ``expires_at`` (mint time + ``expires_in``).
    """

    access_token: str
    expires_at: float  # unix epoch seconds
    token_type: str = "Bearer"
    scope: str = ""

    def expires_within(self, seconds: float, *, now: float | None = None) -> bool:
        return (now if now is not None else time.time()) >= self.expires_at - seconds

    def __repr__(self) -> str:
        return (
            f"DeveloperToken(access_token={redact(self.access_token)}, "
            f"expires_at={self.expires_at}, token_type={self.token_type!r}, "
            f"scope={self.scope!r})"
        )
