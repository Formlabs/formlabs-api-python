"""Blocking access to the async implementation.

The blocking client and its children run the async objects on a private event
loop in a daemon thread and block on the results. Exceptions cross the thread
boundary unchanged, so both clients raise the same errors.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import logging
import queue
import threading
import weakref
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

logger = logging.getLogger("formlabs_sdk.sync")

T = TypeVar("T")
_DONE = object()
# Waits are sliced so a KeyboardInterrupt can be delivered on every platform.
_WAIT_SLICE = 0.25


class CallbackQueue:
    """Hands callbacks fired on the loop thread to the blocked caller's thread.

    ``wrap(callback)`` returns a stand-in that enqueues each call; ``LoopThread.run``
    drains the queue while it waits, invoking the real callback on the calling
    thread.
    """

    def __init__(self) -> None:
        self._queue: queue.SimpleQueue[Any] = queue.SimpleQueue()

    def wrap(self, callback: Callable[..., object]) -> Callable[..., None]:
        def enqueue(*args: Any) -> None:
            self._queue.put((callback, args))

        return enqueue


def _wait(future: concurrent.futures.Future[T]) -> T:
    # Poll on completion rather than on the exception type: the coroutine's
    # own TimeoutError is the same class as the wait's.
    while not future.done():
        concurrent.futures.wait([future], timeout=_WAIT_SLICE)
    return future.result()


def _join(thread: threading.Thread) -> None:
    while thread.is_alive():
        thread.join(_WAIT_SLICE)


def _stop_loop(loop: asyncio.AbstractEventLoop, thread: threading.Thread) -> None:
    """Cancel what is still running, stop the loop, and join its thread.

    Module-level so a ``LoopThread``'s finalizer can call it without keeping
    the ``LoopThread`` alive. Called on the loop's own thread (a finalizer
    running there), it can only ask the loop to stop.
    """
    if loop.is_closed():
        return
    if threading.current_thread() is thread:
        loop.call_soon(loop.stop)
        return

    async def shutdown() -> None:
        current = asyncio.current_task()
        pending = [t for t in asyncio.all_tasks() if t is not current]
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        await loop.shutdown_asyncgens()

    if loop.is_running():
        _wait(asyncio.run_coroutine_threadsafe(shutdown(), loop))
        loop.call_soon_threadsafe(loop.stop)
    _join(thread)
    loop.close()


class LoopThread:
    """A private event loop running on a daemon thread.

    Handles that hold ``aclose()``-able async objects register as owners;
    ``close()`` closes them first, then stops the loop for good. The loop also
    stops itself when the last handle holding it is garbage collected.
    """

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, name="formlabs-sdk", daemon=True
        )
        self._thread.start()
        self._closed = False
        self._lock = threading.Lock()
        self._owners: list[weakref.ref[SyncOwner]] = []
        self._finalizer = weakref.finalize(self, _stop_loop, self._loop, self._thread)
        self._finalizer.atexit = False

    @property
    def closed(self) -> bool:
        return self._closed

    def adopt_owner(self, owner: SyncOwner) -> None:
        with self._lock:
            self._owners.append(weakref.ref(owner))

    def release_owner(self, owner: SyncOwner) -> None:
        with self._lock:
            self._owners = [ref for ref in self._owners if ref() is not owner]

    def run(
        self,
        coro: Coroutine[Any, Any, T],
        *,
        callbacks: CallbackQueue | None = None,
    ) -> T:
        """Run ``coro`` on the loop and block until it finishes.

        A ``KeyboardInterrupt`` (or any exception) on the calling thread
        cancels the coroutine before propagating. With ``callbacks``, the
        queue is drained while waiting so wrapped callbacks run here; a
        callback that raises cancels the coroutine and propagates.
        """
        if threading.current_thread() is self._thread:
            coro.close()
            raise RuntimeError(
                "cannot block on the SDK's own event-loop thread; use the async client "
                "from code that runs there"
            )
        with self._lock:
            if self._closed:
                coro.close()
                raise RuntimeError("this client has been closed")
            future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            if callbacks is None:
                return _wait(future)
            pending = callbacks._queue
            future.add_done_callback(lambda _f: pending.put(_DONE))
            while True:
                try:
                    item = pending.get(timeout=_WAIT_SLICE)
                except queue.Empty:
                    continue
                if item is _DONE:
                    return future.result()
                callback, args = item
                callback(*args)
        except BaseException:
            future.cancel()
            raise

    def close(self) -> None:
        """Close every owner still registered, then stop the loop. Final."""
        if self._closed:
            return
        if threading.current_thread() is self._thread:
            raise RuntimeError("cannot close the SDK's event loop from its own thread")
        with self._lock:
            owners = [owner for ref in reversed(self._owners) if (owner := ref()) is not None]
        for owner in owners:
            try:
                owner._close_async()
            except Exception as exc:
                logger.warning("closing %s failed: %s", type(owner).__name__, exc)
        with self._lock:
            if self._closed:
                return
            self._closed = True
            self._owners.clear()
            self._finalizer.detach()
            _stop_loop(self._loop, self._thread)


class SyncHandle:
    """Base of every blocking twin: the async object plus the loop thread that runs it.

    A handle created by the client, or handed out by another handle, shares
    that owner's loop and lives as long as it does. A handle constructed
    standalone owns a loop, started on first use and stopped for good by
    ``close()``.
    """

    _async: Any
    _loop: LoopThread | None
    _owns_loop: bool

    def __init__(self, async_obj: Any, loop: LoopThread) -> None:
        self._attach(async_obj, loop)

    @classmethod
    def _wrap(cls, async_obj: Any, loop: LoopThread) -> Any:
        handle = cls.__new__(cls)
        handle._attach(async_obj, loop)
        return handle

    def _attach(self, async_obj: Any, loop: LoopThread | None) -> None:
        self._async = async_obj
        self._loop = loop
        self._owns_loop = loop is None
        self._closed = False
        self._start_lock = threading.Lock()

    def _register(self, loop: LoopThread) -> None:
        pass

    @property
    def _runner(self) -> LoopThread:
        loop = self._loop
        if loop is not None:
            return loop
        with self._start_lock:
            if self._closed:
                raise RuntimeError("this handle has been closed")
            if self._loop is None:
                self._loop = LoopThread()
                self._register(self._loop)
            return self._loop

    def _run(self, coro: Coroutine[Any, Any, T], *, callbacks: CallbackQueue | None = None) -> T:
        try:
            runner = self._runner
        except BaseException:
            coro.close()
            raise
        return runner.run(coro, callbacks=callbacks)

    def _run_progress(
        self,
        fn: Callable[..., Coroutine[Any, Any, T]],
        on_progress: Callable[[float], None] | None,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """Run ``fn(*args, on_progress=..., **kwargs)`` with ``on_progress`` on this thread."""
        if on_progress is None:
            return self._run(fn(*args, on_progress=None, **kwargs))
        callbacks = CallbackQueue()
        coro = fn(*args, on_progress=callbacks.wrap(on_progress), **kwargs)
        return self._run(coro, callbacks=callbacks)

    def __repr__(self) -> str:
        return repr(self._async).replace(type(self._async).__name__, type(self).__name__, 1)


class SyncOwner(SyncHandle):
    """A blocking twin whose async object has ``aclose()``; usable as a context manager.

    Registers with its loop, so closing the loop's owner (the client, or a
    shared session) closes it too.
    """

    def _attach(self, async_obj: Any, loop: LoopThread | None) -> None:
        super()._attach(async_obj, loop)
        if loop is not None:
            loop.adopt_owner(self)

    def _register(self, loop: LoopThread) -> None:
        loop.adopt_owner(self)

    def _close_async(self) -> None:
        loop = self._loop
        if loop is None or loop.closed:
            return
        loop.release_owner(self)
        loop.run(self._async.aclose())

    def close(self) -> None:
        """Close the async twin. A handle that owns its thread stops it and cannot be used again."""
        with self._start_lock:
            if self._owns_loop:
                if self._closed:
                    return
                self._closed = True
        try:
            self._close_async()
        finally:
            if self._owns_loop and self._loop is not None:
                self._loop.close()

    def __enter__(self) -> Any:
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.close()


def adopt(obj: Any) -> tuple[Any, LoopThread | None]:
    """Split a constructor argument into the async object and the loop to run on.

    One of this package's blocking twins contributes its loop, so a shared
    blocking session and the handle that borrows it never run on two loops.
    Anything else is passed through with no loop.
    """
    if isinstance(obj, SyncHandle):
        return obj._async, obj._runner
    return obj, None
