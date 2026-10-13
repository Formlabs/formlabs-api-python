"""Live smoke test for client.auth (AsyncFormlabsSession) against production.

Hits https://api.formlabs.com with credentials read from env vars:

    FL_TEST_USER        account email       -> user token
    FL_TEST_PASS        account password    -> user token
    FL_TEST_CLIENT_ID   developer client id -> developer token
    FL_TEST_SECRET      developer secret    -> developer token

Run:  python PreFormAPI/examples/smoke_tests/live_auth_smoke.py

Exercises: user-token mint, JWT exp decoding, a forced refresh via
/o/token/refresh/, developer-token mint, and developer-token revocation on
close.
"""

import asyncio
import datetime
import os
import sys

from formlabs_sdk import AsyncFormlabsClient, FormlabsCredentials, TokenKind, UserToken
from formlabs_sdk.auth.tokens import redact


def env(name: str) -> str | None:
    value = os.environ.get(name)
    return value if value else None


async def main() -> int:
    creds = FormlabsCredentials(
        username=env("FL_TEST_USER"),
        password=env("FL_TEST_PASS"),
        client_id=env("FL_TEST_CLIENT_ID"),
        client_secret=env("FL_TEST_SECRET"),
    )
    missing = [
        name
        for name, value in (
            ("FL_TEST_USER", creds.username),
            ("FL_TEST_PASS", creds.password),
            ("FL_TEST_CLIENT_ID", creds.client_id),
            ("FL_TEST_SECRET", creds.client_secret),
        )
        if not value
    ]
    if missing:
        print(f"missing env vars: {', '.join(missing)}")
        return 2

    async with AsyncFormlabsClient(credentials=creds) as client:
        session = client.auth

        # 1. User token: mint + local exp decode
        access = await session.user_token()
        cached = session._store.load(TokenKind.USER)
        assert isinstance(cached, UserToken)
        expires = datetime.datetime.fromtimestamp(
            cached.expires_at, tz=datetime.timezone.utc
        )
        days = (cached.expires_at - datetime.datetime.now(tz=datetime.timezone.utc).timestamp()) / 86400
        print(f"[ok] user token minted: {redact(access)}")
        print(f"     expires {expires:%Y-%m-%d %H:%M}Z (~{days:.0f} days)")

        # 2. Forced refresh: age the cached token into the skew window so the
        #    next call must go through /o/token/refresh/
        session._store.save(
            TokenKind.USER,
            UserToken(
                access=cached.access,
                refresh=cached.refresh,
                expires_at=datetime.datetime.now(tz=datetime.timezone.utc).timestamp() + 60,
            ),
        )
        refreshed = await session.user_token()
        if refreshed != access:
            print(f"[ok] user token refreshed:  {redact(refreshed)}")
        else:
            print("[??] refresh returned the identical access token")
        after = session._store.load(TokenKind.USER)
        assert isinstance(after, UserToken)
        print(f"     refresh token rotated: {after.refresh != cached.refresh}")

        # 3. Developer token: mint
        dev = await session.developer_token()
        print(f"[ok] developer token minted: {redact(dev)}")

        print("closing client (revokes developer token best-effort)...")

    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
