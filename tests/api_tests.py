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

def _get_pcurrency_json(name, amount):
    return {"currencyname": "{}".format(name), "currencyamount": "{}".format(amount)}

def _get_account_json(name, password):
    return {"name": "{}".format(name), "password": "{}".format(password)}

def check_namespace(client, response):
    ns_href = response["@namespaces"]["crymo"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200

def _check_control_get_method(ctrl, client, obj):
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200

def _check_control_delete_method(ctrl, client, obj):
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204

def _check_control_put_method_pcurrency(ctrl, client, obj):
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_pcurrency_json("LTC", "200.0")
    body["currencyname"] = obj["currencyname"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

def _check_control_put_method_account(ctrl, client, obj):
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_account_json("pekka", "testpwd")
    body["name"] = obj["name"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

def _check_control_post_method_pcurrency(ctrl, client, obj):
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_pcurrency_json("LTC", "200.0")
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201

def _check_control_post_method_account(ctrl, client, obj):
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_account_json("pekka", "testpwd")
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201