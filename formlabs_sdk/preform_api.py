"""Ergonomic layer over the generated PreForm API v1 client (``formlabs_preform_api``).

``AsyncPreFormApi`` is the ``preform`` child of ``AsyncFormlabsClient``:
``launch()`` starts an SDK-owned PreFormServer process, ``connect()`` attaches
to one already running (your own, or the instance bundled with the PreForm
GUI). Both bind the handle in place and return it. The handle raises
``PreFormApiError`` instead of returning the generated ``Error`` model, and
``run()`` turns any ``?async=true`` endpoint into a single awaitable.
``PreFormApi`` is the blocking twin used by ``FormlabsClient``.

The generated client under ``formlabs_preform_api`` stays usable on its own;
``call()`` and ``run()`` accept its operation modules directly.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import sys
from collections import deque
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import httpx

from ._preform_api_facade import AsyncPreFormApiFacade, PreFormApiFacade
from ._sync import SyncHandle, SyncOwner, adopt
from .auth import MissingCredentialsError
from .errors import FormlabsError
from formlabs_preform_api import Client
from formlabs_preform_api.api.authentication import get_user_info as _get_user_info
from formlabs_preform_api.api.authentication import login as _login
from formlabs_preform_api.api.operations import get_operation as _get_operation
from formlabs_preform_api.api.server_info import get_server_version as _get_server_version
from formlabs_preform_api.models import AccessToken, Error, GetOperationMode, UserInfo, UsernameAndPassword
from formlabs_preform_api.models import OperationAccepted
from formlabs_preform_api.types import Unset

DEFAULT_PORT = 44388
DEFAULT_STARTUP_TIMEOUT = 60.0
# The spec documents a 10-minute server-side bound for synchronous long calls.
DEFAULT_TIMEOUT = 605.0
DEFAULT_POLL_INTERVAL = 0.5

_DATA_DIR_VARIABLE = "PREFORM_ENV_DATA_DIRECTORY"
_READY_SENTINEL = "READY FOR INPUT"
_PORT_IN_USE_SENTINEL = "address is already in use"
_OUTPUT_TAIL_LINES = 100
_TERMINATE_GRACE = 10.0


class PreFormApiError(FormlabsError):
    """A PreForm API call failed.

    ``code`` is the server's error code — an open string set (the spec's
    ``ErrorCode``); match on it, never on ``message``. Seven codes are
    client-side, raised without a server error envelope: ``STARTUP_FAILED``,
    ``PORT_IN_USE``, ``SERVER_UNREACHABLE``, ``NOT_CONNECTED`` (no server
    bound yet), ``ALREADY_CONNECTED``, ``NOT_OWNED`` (the handle did not
    launch the server it is bound to), and ``LOGIN_FAILED`` (no user token
    could be obtained for the server).
    ``status_code`` is the HTTP status, or ``None`` when the failure came
    from a polled async operation or from process startup.
    """

    def __init__(self, code: str, message: str, *, status_code: int | None = None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.status_code = status_code


@dataclass(frozen=True)
class _LaunchArgs:
    """What ``launch()`` started the process with; ``restart()`` starts it again with the same."""

    exe_path: str
    port: int
    startup_timeout: float
    timeout: float
    env: dict[str, str] | None
    extra_env: dict[str, str] | None
    data_dir: str | None
    login: bool
    poll_interval: float


def _set_variables(environment: dict[str, str], variables: Mapping[str, str]) -> dict[str, str]:
    if sys.platform == "win32":
        # Variable names are case-insensitive on Windows: Path replaces PATH.
        replaced = {name.upper() for name in variables}
        environment = {name: value for name, value in environment.items() if name.upper() not in replaced}
    environment.update(variables)
    return environment


def _process_env(
    env: Mapping[str, str] | None,
    extra_env: Mapping[str, str] | None,
    data_dir: str | os.PathLike[str] | None,
) -> dict[str, str] | None:
    """The launched process's environment, or ``None`` to inherit this process's."""
    if env is None and extra_env is None and data_dir is None:
        return None
    merged = dict(env) if env is not None else _set_variables(dict(os.environ), extra_env or {})
    if data_dir is not None:
        merged = _set_variables(merged, {_DATA_DIR_VARIABLE: os.fspath(data_dir)})
    return merged


class AsyncPreFormApi(AsyncPreFormApiFacade):
    """Handle to the PreForm API of a PreFormServer process.

    The client constructs it unbound as ``client.preform``. ``launch(exe)``
    or ``connect()`` binds it and returns it, so
    ``async with await client.preform.launch(exe) as preform:`` scopes the
    server's lifetime to a block.

    Every PreForm API operation is a typed method on the handle — e.g.
    ``await preform.create_scene(machine_type=..., ...)`` — generated in
    ``_preform_api_facade.py``; before binding they raise ``PreFormApiError``
    with code ``NOT_CONNECTED``. ``call()`` / ``run()`` remain as the escape
    hatch.

    ``launch(exe, reuse_existing=True)`` attaches to a server already on the
    port and launches one otherwise; ``owns_process`` says which happened.
    For a server the handle launched, ``is_running`` and ``returncode``
    report whether the process has exited, and ``restart()`` replaces it
    with a new one while keeping the handle object bound.

    Closing terminates the server process only when this handle started it
    (``owns_process``); a connected instance is never touched. A closed handle
    can be launched or connected again.
    """

    def __init__(self, *, session: Any = None) -> None:
        self._session = session
        self.client: Client | None = None
        self.base_url: str | None = None
        self.version: str = ""
        self._process: asyncio.subprocess.Process | None = None
        self._drain_task: asyncio.Task[None] | None = None
        self._launch_args: _LaunchArgs | None = None
        self._poll_interval = DEFAULT_POLL_INTERVAL
        self._bind_lock = asyncio.Lock()

    @property
    def session(self) -> Any:
        """The session ``launch()`` and ``login()`` draw the user token from."""
        return self._session

    @property
    def connected(self) -> bool:
        return self.client is not None

    @property
    def owns_process(self) -> bool:
        return self._process is not None

    @property
    def pid(self) -> int | None:
        """Pid of the SDK-owned PreFormServer process, or ``None`` for a
        connected or unbound handle."""
        return self._process.pid if self._process is not None else None

    @property
    def returncode(self) -> int | None:
        """Exit code of the SDK-owned PreFormServer process once it has exited.

        ``None`` while it runs, and for a connected or unbound handle.
        """
        return self._process.returncode if self._process is not None else None

    @property
    def is_running(self) -> bool:
        """Whether the SDK-owned PreFormServer process is still running.

        ``False`` for a connected or unbound handle: the SDK cannot observe a
        process it did not start. To check a connected server, make a call.
        """
        return self._process is not None and self._process.returncode is None

    @property
    def poll_interval(self) -> float:
        """Seconds between polls of an ``?async=true`` operation when a call passes none.

        ``launch()`` and ``connect()`` set it, and ``restart()`` keeps it.
        """
        return self._poll_interval

    def _bind(
        self,
        client: Client,
        *,
        base_url: str,
        process: asyncio.subprocess.Process | None = None,
        drain_task: asyncio.Task[None] | None = None,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> "AsyncPreFormApi":
        self._require_unbound()
        self.client = client
        self.base_url = base_url
        self._process = process
        self._drain_task = drain_task
        self._poll_interval = poll_interval
        return self

    def _require_unbound(self) -> None:
        if self.client is not None:
            raise PreFormApiError(
                "ALREADY_CONNECTED",
                f"this handle is already bound to {self.base_url}; call aclose() first",
            )

    def _require_client(self) -> Client:
        if self.client is None:
            raise PreFormApiError(
                "NOT_CONNECTED", "no PreFormServer is bound; call launch() or connect() first"
            )
        return self.client

    async def launch(
        self,
        exe_path: str | os.PathLike[str],
        *,
        port: int = DEFAULT_PORT,
        startup_timeout: float = DEFAULT_STARTUP_TIMEOUT,
        timeout: float = DEFAULT_TIMEOUT,
        env: Mapping[str, str] | None = None,
        extra_env: Mapping[str, str] | None = None,
        data_dir: str | os.PathLike[str] | None = None,
        login: bool | None = None,
        reuse_existing: bool = False,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> "AsyncPreFormApi":
        """Start a PreFormServer process and wait until it accepts requests.

        Waits for the ``READY FOR INPUT`` line on stdout (bounded by
        ``startup_timeout``), then confirms reachability via ``GET /v1/``.
        The handle owns the process and terminates it on close.

        ``reuse_existing=True`` first connects to a PreFormServer already
        answering on ``port``, as :meth:`connect` would; ``owns_process`` is
        then ``False``, and the arguments for starting a process go unused. Only
        ``SERVER_UNREACHABLE`` falls through to starting one: any other
        failure leaves the handle unbound and re-raises.

        ``login`` logs the server in with the attached session's user token
        when the session has credentials; without a session or credentials
        the server is left logged out. The default, ``None``, logs in a
        server this call started and leaves a reused one as it is. A login
        failure on a started server raises ``PreFormApiError`` and leaves it
        running, logged out, and bound; fix the credentials and call
        :meth:`login`.

        ``env`` is the complete environment for the process (as with
        ``asyncio.create_subprocess_exec``). ``extra_env`` gives the process
        this process's environment plus these variables. Pass one or neither;
        with neither, the process inherits this process's environment.
        ``data_dir`` sets PreFormServer's data directory,
        ``PREFORM_ENV_DATA_DIRECTORY``, in either.

        ``poll_interval`` is the handle's default for every ``?async=true``
        call until it is closed.
        """
        if env is not None and extra_env is not None:
            raise TypeError("pass env= (the whole environment) or extra_env= (merged over os.environ), not both")
        args = _LaunchArgs(
            exe_path=str(exe_path),
            port=port,
            startup_timeout=startup_timeout,
            timeout=timeout,
            env=dict(env) if env is not None else None,
            extra_env=dict(extra_env) if extra_env is not None else None,
            data_dir=os.fspath(data_dir) if data_dir is not None else None,
            login=login is not False,
            poll_interval=poll_interval,
        )
        async with self._bind_lock:
            self._require_unbound()
            if reuse_existing:
                try:
                    return await self._connect_locked(
                        f"http://localhost:{port}",
                        timeout=timeout,
                        login=login is True,
                        poll_interval=poll_interval,
                    )
                except BaseException as exc:
                    if not (isinstance(exc, PreFormApiError) and exc.code == "SERVER_UNREACHABLE"):
                        await self.aclose()
                        raise
            return await self._launch_locked(args)

    async def _launch_locked(self, args: _LaunchArgs) -> "AsyncPreFormApi":
        process = await asyncio.create_subprocess_exec(
            args.exe_path,
            "--port",
            str(args.port),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=_process_env(args.env, args.extra_env, args.data_dir),
        )
        tail: deque[str] = deque(maxlen=_OUTPUT_TAIL_LINES)
        try:
            await asyncio.wait_for(
                self._wait_until_ready(process, tail, args.port), args.startup_timeout
            )
        except asyncio.TimeoutError:
            await self._reap(process)
            raise PreFormApiError(
                "STARTUP_FAILED",
                f"PreFormServer did not print {_READY_SENTINEL!r} within "
                f"{args.startup_timeout}s. Output tail:\n{''.join(tail)}",
            ) from None
        except BaseException:
            await self._reap(process)
            raise

        base_url = f"http://localhost:{args.port}"
        assert process.stdout is not None
        self._bind(
            self._make_client(base_url, args.timeout),
            base_url=base_url,
            process=process,
            drain_task=asyncio.get_running_loop().create_task(
                self._drain(process.stdout, tail)
            ),
            poll_interval=args.poll_interval,
        )
        self._launch_args = args
        try:
            self.version = await self._probe()
        except BaseException:
            await self.aclose()
            raise
        if args.login:
            await self._login_if_possible()
        return self

    async def connect(
        self,
        *,
        port: int = DEFAULT_PORT,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        login: bool = False,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> "AsyncPreFormApi":
        """Attach to a PreFormServer someone else is running.

        Verifies it via ``GET /v1/``. The handle never terminates the
        process and, unless ``login=True``, never touches its login state —
        check ``current_user()`` before replacing a session someone may be
        using. ``login=True`` behaves as in :meth:`launch`, as does
        ``poll_interval``.
        """
        async with self._bind_lock:
            return await self._connect_locked(
                base_url or f"http://localhost:{port}",
                timeout=timeout,
                login=login,
                poll_interval=poll_interval,
            )

    async def _connect_locked(
        self, base_url: str, *, timeout: float, login: bool, poll_interval: float
    ) -> "AsyncPreFormApi":
        self._bind(
            self._make_client(base_url, timeout), base_url=base_url, poll_interval=poll_interval
        )
        try:
            self.version = await self._probe()
        except (httpx.HTTPError, PreFormApiError, ValueError) as exc:
            await self.aclose()
            raise PreFormApiError(
                "SERVER_UNREACHABLE",
                f"no PreFormServer reachable at {base_url}: {exc}",
            ) from exc
        except BaseException:
            await self.aclose()
            raise
        if login:
            await self._login_if_possible()
        return self

    async def restart(self) -> "AsyncPreFormApi":
        """Terminate the server process this handle launched and start it again.

        The new process gets the same executable, port, environment arguments,
        login behavior, and poll interval, and binds this same handle, so existing
        references to it stay valid. It also replaces a process that has
        exited (``is_running`` is ``False``). A process that fails to start
        leaves the handle unbound, as in :meth:`launch`.

        Raises ``PreFormApiError`` with code ``NOT_CONNECTED`` on an unbound
        handle and ``NOT_OWNED`` on a handle bound to a server it did not
        launch (``connect()``, or ``launch(reuse_existing=True)`` that found
        one).
        """
        async with self._bind_lock:
            self._require_client()
            args = self._launch_args
            if args is None:
                raise PreFormApiError(
                    "NOT_OWNED",
                    f"this handle did not launch the server at {self.base_url}, so it cannot restart it",
                )
            await self.aclose()
            return await self._launch_locked(args)

    async def _login_if_possible(self) -> bool:
        """Log in with the attached session; ``False`` when there is no
        session or it has no credentials to mint a token from.

        Any other failure to obtain a token raises ``LOGIN_FAILED``; a token
        the server rejects raises the server's own error. The server keeps
        running either way.
        """
        if self._session is None:
            return False
        try:
            token = await self._session.user_token()
        except MissingCredentialsError:
            return False
        except Exception as exc:
            raise PreFormApiError(
                "LOGIN_FAILED",
                f"PreFormServer is running but could not be logged in: {exc}",
            ) from exc
        await self.call(_login, body=AccessToken(token))
        return True

    async def call(self, operation_module: ModuleType, /, **kwargs: Any) -> Any:
        """Invoke a generated operation module, raising on error responses.

        ``await server.call(list_scenes)`` ≡ ``list_scenes.asyncio(...)``,
        except an ``Error`` result becomes a raised ``PreFormApiError``.
        """
        client = self._require_client()
        response = await operation_module.asyncio_detailed(client=client, **kwargs)
        parsed = response.parsed
        if isinstance(parsed, Error):
            raise PreFormApiError(
                parsed.error.code,
                parsed.error.message,
                status_code=int(response.status_code),
            )
        return parsed

    async def run(
        self,
        operation_module: ModuleType,
        /,
        *,
        poll_interval: float | None = None,
        timeout: float | None = None,
        on_progress: Callable[[float], None] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Run a ``?async=true``-capable operation to completion.

        Starts the operation with ``async_=True`` and polls
        ``/v1/operation/get/?mode=oneshot`` every ``poll_interval`` seconds
        (``None`` uses the handle's :attr:`poll_interval`) until it finishes
        (``oneshot`` deletes the finished record server-side, so no cleanup
        call is needed). Returns the operation's ``result`` as a plain dict (``None``
        when the endpoint's success response has no body). A ``FAILED``
        operation raises ``PreFormApiError`` from the embedded error envelope;
        an unrecognized future status is treated as still running. ``timeout``
        bounds the polling, including an in-flight poll, raising
        ``TimeoutError``. ``on_progress`` is called from the polling loop with
        each increase of the operation's ``progress`` value; it should return
        quickly and not raise.
        """
        interval = self._poll_interval if poll_interval is None else poll_interval
        started = await self.call(operation_module, async_=True, **kwargs)
        if not isinstance(started, OperationAccepted):
            return started  # server chose to answer synchronously
        operation_id = started.operation_id
        status = "unknown"
        last_progress = float("-inf")

        async def poll() -> Any:
            nonlocal status, last_progress
            while True:
                op = await self.call(
                    _get_operation, operation_id=operation_id, mode=GetOperationMode.ONESHOT
                )
                status = op.status
                if on_progress is not None and op.progress > last_progress:
                    last_progress = op.progress
                    on_progress(op.progress)
                result = {} if isinstance(op.result, Unset) else op.result.additional_properties
                if status == "SUCCEEDED":
                    return result or None
                if status == "FAILED":
                    detail = result.get("error") or {}
                    raise PreFormApiError(
                        detail.get("code", "UNKNOWN_FAILURE"),
                        detail.get("message", "operation failed with no error detail"),
                    )
                await asyncio.sleep(interval)

        try:
            return await asyncio.wait_for(poll(), timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"operation {operation_id} still {status} after {timeout}s"
            ) from None

    async def login(
        self,
        token_or_session: Any = None,
        /,
        *,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Log the server in.

        With no arguments, uses the attached session. Otherwise pass a user
        access token string, a session (anything with an async
        ``user_token()``), or ``username=`` and ``password=`` keywords.
        """
        if token_or_session is not None and (username is not None or password is not None):
            raise TypeError("login() takes a token/session or username/password, not both")
        if token_or_session is None and username is None and password is None:
            if self._session is None:
                raise TypeError(
                    "login() requires a token/session, or both username= and password= "
                    "(this handle has no session attached)"
                )
            token_or_session = self._session
        body: AccessToken | UsernameAndPassword
        if token_or_session is not None:
            if isinstance(token_or_session, str):
                body = AccessToken(token_or_session)
            else:
                user_token = getattr(token_or_session, "user_token", None)
                if not callable(user_token):
                    raise TypeError(
                        "login() expects a token string or an object with an async "
                        f"user_token() method, not {type(token_or_session).__name__}"
                    )
                body = AccessToken(await user_token())
        elif username is not None and password is not None:
            body = UsernameAndPassword(username=username, password=password)
        else:
            raise TypeError("login() requires a token/session, or both username= and password=")
        await self.call(_login, body=body)

    async def current_user(self) -> UserInfo | None:
        """Who is logged in on this server, or ``None`` if no one is."""
        response = await _get_user_info.asyncio_detailed(client=self._require_client())
        if response.status_code == 404:
            return None
        parsed = response.parsed
        if isinstance(parsed, Error):
            raise PreFormApiError(
                parsed.error.code,
                parsed.error.message,
                status_code=int(response.status_code),
            )
        return parsed

    async def aclose(self) -> None:
        """Unbind the handle; terminate the server process only if this handle started it.

        Idempotent. The handle can be launched or connected again afterwards.
        """
        process, self._process = self._process, None
        if process is not None and process.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                process.terminate()
            try:
                await asyncio.wait_for(process.wait(), _TERMINATE_GRACE)
            except asyncio.TimeoutError:
                with contextlib.suppress(ProcessLookupError):
                    process.kill()
                await process.wait()
        # The drain runs until the process has exited, so shutdown output
        # cannot fill the pipe and block it.
        if self._drain_task is not None:
            self._drain_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._drain_task
            self._drain_task = None
        client, self.client = self.client, None
        self.base_url = None
        self.version = ""
        self._launch_args = None
        self._poll_interval = DEFAULT_POLL_INTERVAL
        if client is not None:
            await client.get_async_httpx_client().aclose()

    async def __aenter__(self) -> "AsyncPreFormApi":
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.aclose()

    async def _probe(self) -> str:
        info = await self.call(_get_server_version)
        return info.version

    @staticmethod
    def _make_client(base_url: str, timeout: float) -> Client:
        return Client(base_url=base_url, timeout=httpx.Timeout(timeout, connect=10.0))

    @staticmethod
    async def _wait_until_ready(
        process: asyncio.subprocess.Process, tail: deque[str], port: int
    ) -> None:
        assert process.stdout is not None
        while True:
            raw = await process.stdout.readline()
            if not raw:
                raise PreFormApiError(
                    "STARTUP_FAILED",
                    "PreFormServer exited before printing "
                    f"{_READY_SENTINEL!r}. Output tail:\n{''.join(tail)}",
                )
            line = raw.decode(errors="replace")
            tail.append(line)
            if _READY_SENTINEL in line:
                return
            if _PORT_IN_USE_SENTINEL in line:
                raise PreFormApiError(
                    "PORT_IN_USE",
                    f"port {port} is already in use — another PreFormServer "
                    "(or the PreForm GUI) may be running",
                )

    @staticmethod
    async def _drain(stream: asyncio.StreamReader, tail: deque[str]) -> None:
        # Keep the stdout pipe from filling up; retain a bounded tail.
        while True:
            raw = await stream.readline()
            if not raw:
                return
            tail.append(raw.decode(errors="replace"))

    @staticmethod
    async def _reap(process: asyncio.subprocess.Process) -> None:
        if process.returncode is None:
            with contextlib.suppress(ProcessLookupError):
                process.kill()
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(process.wait(), _TERMINATE_GRACE)


class PreFormApi(SyncOwner, PreFormApiFacade):
    """Blocking twin of :class:`AsyncPreFormApi`; the ``preform`` child of ``FormlabsClient``.

    The same methods, called without ``await``. The async handle runs on the
    client's event-loop thread; ``on_progress`` callbacks run on the calling
    thread. Usable as a context manager: ``with client.preform.launch(exe):``.
    """

    def __init__(self, *, session: Any = None) -> None:
        async_session, loop = adopt(session)
        self._attach(AsyncPreFormApi(session=async_session), loop)

    @property
    def session(self) -> Any:
        return self._async.session

    @property
    def connected(self) -> bool:
        return self._async.connected

    @property
    def owns_process(self) -> bool:
        return self._async.owns_process

    @property
    def pid(self) -> int | None:
        return self._async.pid

    @property
    def returncode(self) -> int | None:
        return self._async.returncode

    @property
    def is_running(self) -> bool:
        return self._async.is_running

    @property
    def poll_interval(self) -> float:
        return self._async.poll_interval

    @property
    def version(self) -> str:
        return self._async.version

    @property
    def base_url(self) -> str | None:
        return self._async.base_url

    @property
    def client(self) -> Client | None:
        """The generated client; only usable from the SDK's event-loop thread."""
        return self._async.client

    def launch(
        self,
        exe_path: str | os.PathLike[str],
        *,
        port: int = DEFAULT_PORT,
        startup_timeout: float = DEFAULT_STARTUP_TIMEOUT,
        timeout: float = DEFAULT_TIMEOUT,
        env: Mapping[str, str] | None = None,
        extra_env: Mapping[str, str] | None = None,
        data_dir: str | os.PathLike[str] | None = None,
        login: bool | None = None,
        reuse_existing: bool = False,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> "PreFormApi":
        """Start a PreFormServer (or reuse one) and bind to it; see :meth:`AsyncPreFormApi.launch`."""
        self._run(
            self._async.launch(
                exe_path,
                port=port,
                startup_timeout=startup_timeout,
                timeout=timeout,
                env=env,
                extra_env=extra_env,
                data_dir=data_dir,
                login=login,
                reuse_existing=reuse_existing,
                poll_interval=poll_interval,
            )
        )
        return self

    def connect(
        self,
        *,
        port: int = DEFAULT_PORT,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        login: bool = False,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> "PreFormApi":
        """Attach to a running PreFormServer; see :meth:`AsyncPreFormApi.connect`."""
        self._run(
            self._async.connect(
                port=port, base_url=base_url, timeout=timeout, login=login, poll_interval=poll_interval
            )
        )
        return self

    def restart(self) -> "PreFormApi":
        """Start the server this handle launched again; see :meth:`AsyncPreFormApi.restart`."""
        self._run(self._async.restart())
        return self

    def login(
        self,
        token_or_session: Any = None,
        /,
        *,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Log the server in; see :meth:`AsyncPreFormApi.login`."""
        if isinstance(token_or_session, SyncHandle) and hasattr(token_or_session, "user_token"):
            # A blocking session mints on its own thread; hand the server the token.
            token_or_session = token_or_session.user_token()
        self._run(self._async.login(token_or_session, username=username, password=password))

    def current_user(self) -> UserInfo | None:
        """Who is logged in on this server, or ``None`` if no one is."""
        return self._run(self._async.current_user())

    def call(self, operation_module: ModuleType, /, **kwargs: Any) -> Any:
        """Invoke a generated operation module, raising on error responses."""
        return self._run(self._async.call(operation_module, **kwargs))

    def run(
        self,
        operation_module: ModuleType,
        /,
        *,
        poll_interval: float | None = None,
        timeout: float | None = None,
        on_progress: Callable[[float], None] | None = None,
        **kwargs: Any,
    ) -> Any:
        """Run a ``?async=true``-capable operation to completion; see :meth:`AsyncPreFormApi.run`."""
        return self._run_progress(
            self._async.run,
            on_progress,
            operation_module,
            poll_interval=poll_interval,
            timeout=timeout,
            **kwargs,
        )
