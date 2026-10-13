"""Pluggable token persistence.

The default store is in-memory: tokens live for the lifetime of the session
object. Any object implementing the same protocol, such as a file-backed store,
can replace it.
"""

from __future__ import annotations

from typing import Protocol, Union

from .tokens import DeveloperToken, TokenKind, UserToken

Token = Union[UserToken, DeveloperToken]


class TokenStore(Protocol):
    def load(self, kind: TokenKind) -> Token | None: ...

    def save(self, kind: TokenKind, token: Token) -> None: ...

    def clear(self, kind: TokenKind) -> None: ...


class InMemoryTokenStore:
    """Default store: tokens are held in a dict and lost when the session ends."""

    def __init__(self) -> None:
        self._tokens: dict[TokenKind, Token] = {}

    def load(self, kind: TokenKind) -> Token | None:
        return self._tokens.get(kind)

    def save(self, kind: TokenKind, token: Token) -> None:
        self._tokens[kind] = token

    def clear(self, kind: TokenKind) -> None:
        self._tokens.pop(kind, None)
