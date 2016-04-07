import pytest
import factory
from pytest_factoryboy import register
from factory.alchemy import SQLAlchemyModelFactory
from laboratory.fooflask import configure_app, configure_db, Personne, bind_db_to_app
from sqlalchemy.orm import sessionmaker






@pytest.fixture(scope='session')
def app():
    return configure_app()

@pytest.yield_fixture(scope='function', autouse=True)
def db_session(app):
    db = configure_db()
    bind_db_to_app(db, app)
    Session = sessionmaker(bind=db.engine)
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()
    session.close()


@register
class PersonneFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Personne
        sqlalchemy_session = db_session

    name = factory.Sequence(lambda n: 'personne_{}'.format(n))
