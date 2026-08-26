import os
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


_engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///:memory:")


def _normalize(url: str) -> str:
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    scheme, _, rest = url.partition("://")
    if scheme == "postgresql":
        return f"postgresql+psycopg://{rest}"
    return url


def get_engine() -> Engine:
    global _engine, SessionLocal
    if _engine is None:
        url = _normalize(database_url())
        kwargs: dict = {"pool_pre_ping": True}
        if url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
            if ":memory:" in url:
                kwargs["poolclass"] = StaticPool
        _engine = create_engine(url, **kwargs)
        SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def get_session() -> Generator[Session, None, None]:
    get_engine()
    assert SessionLocal is not None
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    from app.models import ApplicationRow  # noqa: F401

    Base.metadata.create_all(bind=get_engine())


def ping() -> None:
    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))
