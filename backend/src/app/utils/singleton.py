"""
``fastapi.Depends`` is called on every request.
This wraps ``fastapi.FastAPI.on_event("startup"|"shutdown")`` and ``fastapi.Depends``,
and provides a single :func:`singleton` decorator to declare a dependency that is
setup and shutdown with the application.

.. note::
    So as to keep things simple, the implementation has one caveat: the dependency is
    systematically setup/shutdown with the application, regardless of whether its
    dependant is called.

.. seealso::
    - https://github.com/tiangolo/fastapi/issues/504
    - https://github.com/tiangolo/fastapi/issues/617
"""
import contextlib
from typing import Any, AsyncGenerator, Callable

import fastapi


def singleton(app: fastapi.FastAPI) -> Any:
    """
    Decorator that can be used to define a resource with the same lifetime as the
    fastapi application.

    :param app: fastapi application.
    :return: A decorator that can be used anywhere ``@contextlib.asynccontextmanager``
        would be used. Specifically, it must be an async generator yielding exactly once.
        The decorated function can then be used where the return value of ``fastapi.Depends()``
        would be used.

    Example::

        from typing import AsyncIterator

        import fastapi

        # For demo purposes
        class Database:
            async def start(): ...
            async def shutdown(): ...

        app = fastapi.FastAPI()

        @singleton(app)
        async def database() -> AsyncIterator[Database]:
            db = Database()
            await db.start()
            yield db
            await db.shutdown()

        @app.get("/users")
        def get_users(db: Database = database):
            ...
    """

    def decorator(func: Callable[[], AsyncGenerator[Any, None]]) -> Any:
        # Don't instantiate the context manager yet, otherwise it can only be used once
        cm_factory = contextlib.asynccontextmanager(func)
        stack = contextlib.AsyncExitStack()
        sentinel_start = object()
        sentinel_shutdown = object()
        value: Any = sentinel_start

        @app.on_event("startup")
        async def _startup() -> None:
            nonlocal value
            value = await stack.enter_async_context(cm_factory())

        @app.on_event("shutdown")
        async def _shutdown() -> None:
            nonlocal value
            await stack.pop_all().aclose()
            value = sentinel_shutdown

        def get_value() -> Any:
            if value is sentinel_start:
                raise RuntimeError("Application not started yet.")
            if value is sentinel_shutdown:
                raise RuntimeError("Application already shut down.")
            return value

        return fastapi.Depends(get_value)

    return decorator