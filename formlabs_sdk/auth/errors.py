"""Exception hierarchy for Formlabs SDK authentication."""

from __future__ import annotations

from ..errors import FormlabsError


class FormlabsAuthError(FormlabsError):
    """Base class for all authentication errors raised by the SDK.

    ``endpoint`` is the URL the failing request was sent to; ``detail`` is the
    server's error payload (``error``/``error_description`` for OAuth endpoints,
    or the SimpleJWT field-error dict), reproduced verbatim. Tokens and secrets
    are never included.
    """

    def __init__(
        self,
        message: str,
        *,
        endpoint: str | None = None,
        detail: str | None = None,
    ) -> None:
        self.endpoint = endpoint
        self.detail = detail
        parts = [message]
        if endpoint:
            parts.append(f"endpoint: {endpoint}")
        if detail:
            parts.append(f"server response: {detail}")
        super().__init__(" | ".join(parts))


class MissingCredentialsError(FormlabsAuthError):
    """A token was requested but the credential pair needed to mint it was not provided."""


class InvalidCredentialsError(FormlabsAuthError):
    """The server rejected the provided credentials when minting a token."""


class TokenRefreshError(FormlabsAuthError):
    """A cached token could not be refreshed or re-minted."""
