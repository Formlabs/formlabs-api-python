# formlabs-sdk

> This is formlabs-sdk v1.0.0-alpha, for PreForm API v1.0.0-alpha (PreForm 3.64.0.661). The SDK is versioned by the API: [every release](https://github.com/Formlabs/formlabs-api-python/releases) is tagged `v<api version>`, or `v<api version>.post<N>` for an SDK-only fix, and [the API v1.0.0-alpha reference](https://developer.formlabs.com/api-reference/v1.0.0-alpha/) stays online after newer ones.

Python SDK for the Formlabs PreForm API. One client holds the account and exposes each API as a child:

| | Blocking | Async |
|---|---|---|
| Client | `FormlabsClient` | `AsyncFormlabsClient` |
| `client.auth` | `FormlabsSession` | `AsyncFormlabsSession` |
| `client.preform` | `PreFormApi` | `AsyncPreFormApi` |

Both clients have the same methods and raise the same errors. The async client's methods are awaited. The examples below use the blocking client.

```python
from formlabs_sdk import FormlabsClient

with FormlabsClient(username="you@example.com", password="...") as client:
    token = client.auth.user_token()   # minted on first use, refreshed before expiry
```

Tokens never appear in logs, exceptions, or `repr` output except as a redacted prefix.

## Install

Python 3.11 or newer.

```
pip install "formlabs-sdk @ git+https://github.com/Formlabs/formlabs-api-python@v1.0.0-alpha#subdirectory=PreFormAPI"
```

## The client

`FormlabsClient(username=..., password=...)`, or `FormlabsClient(credentials=FormlabsCredentials(...))` when you also hold developer credentials. Each child draws its token from `client.auth`. Construction does no I/O.

Credentials are optional. Without them an unauthenticated PreFormServer still works, and anything that needs the account raises `MissingCredentialsError`.

Environment settings go on the constructor: `api_base_url`, `http_client`, `store`, and `refresh_skew`. Pass `session=` to share one session between clients; the client then leaves it open on close.

Closing the client (`with` exit or `close()`; `aclose()` on the async client) terminates a PreFormServer the SDK launched, then closes an owned session. The blocking client also stops its event-loop thread, so a closed client cannot be reused. Each child can be closed on its own and launched or connected again.

Each child can also be constructed on its own, for example to drive a second PreFormServer: `PreFormApi(session=client.auth).launch(exe, port=44389)`. Given the client's session it runs on the client's thread and closes with the client. Built without one, a blocking child owns its own thread, and once closed it cannot be reused.

Every API and authentication error derives from `FormlabsError`. Timeouts raise the builtin `TimeoutError`.

## PreForm API

`client.preform` drives a local `PreFormServer` process over its REST API. `launch(exe)` starts an SDK-owned process; `connect()` attaches to one already running, such as the instance bundled with the PreForm GUI. Both bind the child and return it. Until one of them has run, every other method raises `PreFormApiError` with code `NOT_CONNECTED`.

```python
with FormlabsClient(username="you@example.com", password="...") as client:
    preform = client.preform.launch(r"C:\...\PreFormServer.exe")

    scene = preform.create_scene(
        machine_type="FORM-4-0", material_code="FLGPGR05", layer_thickness_mm=0.1
    )
    preform.import_models(scene_id=scene.scene_id, file="part.stl")
    report = preform.validate_manifoldness(scene_id=scene.scene_id)
```

`launch()` logs the server in with the client's account; without credentials the server stays logged out. Pass `login=False` to skip the login. If the login fails, for example because the account cannot be reached, the server keeps running logged out and `launch()` raises `PreFormApiError`; call `preform.login()` once the problem is fixed. `connect()` does not touch the login state of a server it did not start unless you pass `login=True`; check `preform.current_user()` before replacing the login of a shared instance. `preform.login()` logs in later, with the client's account, a token string, or `username=` and `password=`.

Methods are named after the API's operationIds (`create_scene`, `import_models`, `validate_minima`, ...) and take the request's fields as keyword arguments, so the surface is discoverable from autocomplete. Structured values (positions, orientations, drain holes) take the model classes from `formlabs_preform_api.models`. Endpoints with alternative request forms accept either set of arguments: `create_scene(machine_type=..., ...)` or `create_scene(fps_file=...)`. Id-valued arguments accept a `UUID` or its string form. Every operation raises `PreFormApiError` on an error response.

Long-running endpoints are started with `?async=true` and polled to completion behind one call. Their methods also take `poll_interval`, `timeout`, and `on_progress`, a callback fired on each increase of the operation's progress: `preform.print_scene(..., on_progress=lambda p: print(f"{p:.0%}"))`. On the blocking client the callback runs on the calling thread.

`launch` accepts `env` for the server's process environment, and `pid` is the owned process id. `connect(port=44388)` or `connect(base_url=...)` attaches to a server you started yourself. The SDK verifies a server with `GET /v1/` and never terminates a process it did not start. `with client.preform.launch(exe) as preform:` closes the server at the end of the block; the child can be launched again afterwards.

`preform.call(module, **kwargs)` invokes any operation module under `formlabs_preform_api.api.<tag>` with the same raise-on-error behavior, for example `preform.call(print_scene, async_=True, body=...)` to receive the raw `OperationAccepted` and poll yourself.

## Async client

`AsyncFormlabsClient` has the same shape with `await`:

```python
import asyncio
from formlabs_sdk import AsyncFormlabsClient

async def main():
    async with AsyncFormlabsClient(username="you@example.com", password="...") as client:
        async with await client.preform.launch(r"C:\...\PreFormServer.exe") as preform:
            scene = await preform.create_scene(
                machine_type="FORM-4-0", material_code="FLGPGR05", layer_thickness_mm=0.1
            )
            await preform.import_models(scene_id=scene.scene_id, file="part.stl")

asyncio.run(main())
```

The blocking client runs the async client on a private event-loop thread and blocks on each call. Interrupting a blocking call cancels the underlying operation.

