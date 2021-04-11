import pytest
import json
import tempfile
import os

from sqlalchemy.engine import Engine
from jsonschema import validate, ValidationError
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
def client():
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

def _check_namespace(client, response):
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


class TestAccountCollection(object):
	""" 
	Tests of AccountCollection resource.
	""" 
	RESOURCE_URL = "/api/accounts/"

	def test_get(self, client):
		resp = client.get(self.RESOURCE_URL)
		assert resp.status_code == 200
		body = json.loads(resp.data)
		_check_namespace(client, body)
		_check_control_post_method_account("crymo:add-account", client, body)
		assert len (body["items"]) == 3
		for item in body["items"]:
			_check_control_get_method("self", client, item)
			_check_control_get_method("profile", client, item)
	
	def test_post(self, client):
		valid = _get_account_json("juu", 12.5)

		#test with wrong content type
		resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
		assert resp.status_code == 415

		#Test with valid and see if exists afterwards
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 201

		# assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["id"] + "/")
		resp = client.get(resp.headers["Location"])
		assert resp.status_code == 200

		# send same data again for 409
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 409

		# remove model field for 400
		valid.pop("name")
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 400

class TestAccountItem(object):
    """ 
    Test accountitem resource
    """
    RESOURCE_URL = "/api/accounts/test-account-1/"
    INVALID_URL = "/api/accounts/non-account-x/"
    def test_get(self, client):
        pass

    def test_put(self, client):
       pass

    def test_delete(self, client):
       pass

"""
class TestCryptoCurrencyCollection(object):

	def test_get(self, client):
		pass

class TestCryptoCurrencyItem(object):

	def test_get(self, client):
		pass

class TestPortfolioItem(object):

	def test_get(self, client):
		pass

class TestPortfolioCurrencyCollection(object):

	def test_get(self, client):
		pass

	def test_post(self, client):
		pass

class TestPortfolioCurrency(object):

	def test_get(self, client):
		pass

	def test_put(self, client):
		pass

	def test_delete(self, client):
		pass
"""