import pytest
from app import app


@pytest.fixture
def fullapp():
    app.config.update({"TESTING": True})
    return app
