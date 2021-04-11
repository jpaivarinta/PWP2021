import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event
from cryptomonitor import create_app, db
from datetime import datetime
from cryptomonitor.models import UserAccount, Portfolio, CryptoCurrency, crypto_portfolio


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        _populate_db()
        
    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)

def _populate_db():
    for i in range(1, 4):
        a = UserAccount(
            name = "test-account-{}".format(i),
            password = "testpwd"
        )
        p = Portfolio(
            timestamp = datetime.now(),
            value = float(i * 100)
        )
        a.portfolio = p
        db.session.add(a)
        db.session.add(p)
    db.session.commit()

def check_namespace(client, response):
    ns_href = response["@namespaces"]["crymo"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200

