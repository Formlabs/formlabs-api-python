"""Root of the SDK's exception hierarchy."""

from __future__ import annotations


class FormlabsError(Exception):
    """Base class for the SDK's own exceptions.

    Catch this to handle any API or authentication failure in one clause; the
    subclasses, such as ``FormlabsAuthError`` and ``PreFormApiError``, carry
    the details. Timeouts raise the builtin ``TimeoutError``, and misuse of a
    closed or wrongly threaded blocking handle raises ``RuntimeError``.
    """
