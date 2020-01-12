import pytest

from api.app import create_app
from api.db import db as _db
from api import settings
import os


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app


@pytest.fixture()
def db(app, request):
    """
    Returns session-wide initialised database.
    """
    with app.app_context():
        _db.drop_all()
        _db.create_all()
