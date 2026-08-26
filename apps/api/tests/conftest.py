import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ.pop("REDIS_URL", None)

import pytest
from fastapi.testclient import TestClient

from app.db import Base, get_engine, init_db
from app.main import app


@pytest.fixture(autouse=True)
def _reset_schema():
    init_db()
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
