import tears
import pytest
import threading
from laboratory.fooflask import app as fapp, db


@pytest.fixture(scope='session')
def app():
    return fapp


@pytest.yield_fixture(scope='function', autouse=True)
def db_session(app):
    db.session.bind.setup()
    yield db.session
    db.session.bind.teardown()
