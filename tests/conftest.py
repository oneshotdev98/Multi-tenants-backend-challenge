import os
import sys
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

# Ensure app settings resolve to local test values before importing app modules.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["GOOGLE_API_KEY"] = "test-key"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def assert_is_uuid(value: str):
    UUID(value)
