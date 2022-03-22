import pytest


@pytest.fixture(scope='module')
def conn():
    from conf.databases import default_engine
    connection = default_engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def db(conn):
    from conf.databases import DefaultSession
    transaction = conn.begin()
    db = DefaultSession(bind=conn)
    yield db
    db.close()
    transaction.rollback()
