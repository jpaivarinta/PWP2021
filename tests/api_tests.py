import pytest
import json
import tempfile
import os
import time

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
    cc = _get_CryptoCurrency()
    cc2 = _get_CryptoCurrency2()
    cc3 = _get_CryptoCurrency3()
    db.session.add(cc)
    db.session.add(cc2)
    db.session.add(cc3)

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
        cp = crypto_portfolio(portfolio=p, cryptocurrency=cc, currencyAmount=500.0)
        cp2 = crypto_portfolio(portfolio=p, cryptocurrency=cc2, currencyAmount=47666.0)
        p.cryptocurrencies.append(cp)
        p.cryptocurrencies.append(cp2)
        db.session.add(cp)
        db.session.add(cp2)
        db.session.add(a)
        db.session.add(p)
    db.session.commit()

def _get_pcurrency_json(name, amount):
    return {"currencyname": "{}".format(name), "currencyamount": "{}".format(amount)}

def _get_account_json(name, password):
    return {"name": "{}".format(name), "password": "{}".format(password)}

def _get_CryptoCurrency():
	return CryptoCurrency(
	    name="DogeCoin",
	    abbreviation="DOGE",
	    timestamp=datetime.now(),
	    value=0.0462,
	    daily_growth=7.1,
	    launchDate=datetime(2012,5,12),
	    blockchain_length=3610463
	)

def _get_CryptoCurrency2():
	return CryptoCurrency(
	    name="Bitcoin",
	    abbreviation="BTC",
	    timestamp=datetime.now(),
	    value=50000.00,
	    daily_growth=7.1,
	    launchDate=datetime(2012,5,12),
	    blockchain_length=3610463
	)

def _get_CryptoCurrency3():
	return CryptoCurrency(
	    name="Litecoin",
	    abbreviation="LTC",
	    timestamp=datetime.now(),
	    value=10000.00,
	    daily_growth=2.1,
	    launchDate=datetime(1500,5,12),
	    blockchain_length=3610463
	)

# GENERAL CONTROL CHECKS

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


# ACCOUNT CONTROL CHECKS

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


# PCURRENCY CONTROL CHECKS

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
    # print(href)
    resp = client.post(href, json=body)
    # print(obj)
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
			_check_control_get_method("portfolio", client, item)
	
	def test_post(self, client):
		valid = _get_account_json("juu", "testpwd")
		#print(valid)

		#test with wrong content type
		resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
		assert resp.status_code == 415

		#Test with valid and see if exists afterwards
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 201
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
    """ Tests for AccountItem resource. """
    RESOURCE_URL = "/api/accounts/test-account-1/"
    INVALID_URL = "/api/accounts/non-account-x/"

    def test_get(self, client):
    	""" Tests for GET method of AccountItem resource. """
    	resp = client.get(self.RESOURCE_URL)
    	body = json.loads(resp.data)
    	_check_namespace(client, body)
    	_check_control_get_method("profile", client, body)
    	_check_control_get_method("crymo:accounts-all", client, body)
    	_check_control_put_method_account("edit", client, body)
    	_check_control_delete_method("crymo:delete", client, body)
    	resp = client.get(self.INVALID_URL)
    	assert resp.status_code == 404

    def test_put(self, client):
    	""" Tests for GET method of AccountItem resource. """
    	valid = _get_account_json("pekka", "testpwd")

    	#Test with wrong content type
    	resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
    	assert resp.status_code == 415

    	#Test with another account's name
    	valid["name"] = "test-account-2"
    	resp = client.put(self.RESOURCE_URL, json=valid)
    	assert resp.status_code == 409

    	#Test with valid
    	valid["name"] = "test-account-1"
    	resp = client.put(self.RESOURCE_URL, json=valid)
    	assert resp.status_code == 204

    	#Remove account for 400
    	valid.pop("name")
    	resp = client.put(self.RESOURCE_URL, json=valid)
    	assert resp.status_code == 400

    def test_delete(self, client):
       """ Tests for DELETE method of AccountItem resource. """
       resp = client.delete(self.RESOURCE_URL)
       assert resp.status_code == 204
       resp = client.delete(self.RESOURCE_URL)
       assert resp.status_code == 404
       resp = client.delete(self.INVALID_URL)
       assert resp.status_code == 404



class TestCryptoCurrencyCollection(object):
    """ Test for CryptoCurrencyCollection resource. """ 

    RESOURCE_URL = "/api/currencies/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        for control in body["@controls"]:
            _check_control_get_method(control, client, body)

        for item in body["items"]:
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

class TestCryptoCurrencyItem(object):
    """ Test for CryptoCurrencyItem resource. """

    RESOURCE_URL = "/api/currencies/DOGE/"
    INVALID_URL = "/api/currencies/DOGGO/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        for control in body["@controls"]:
            _check_control_get_method(control, client, body)
        
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

class TestPortfolioItem(object):
    """ 
    Test cryptocurrencycollection
    """ 

    RESOURCE_URL = "/api/accounts/test-account-1/portfolio/"
    INVALID_URL = "/api/accounts/jorma/portfolio/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        for control in body["@controls"]:
            _check_control_get_method(control, client, body)

        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404


class TestPortfolioCurrencyCollection(object):
    
    """ Test portfoliocurrencycollection """
    
    RESOURCE_URL = "/api/accounts/test-account-1/portfolio/pcurrencies/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method_pcurrency("crymo:add-pcurrency", client, body)
        assert len (body["items"]) == 2
        # print(body)
        for item in body["items"]:
            print(item)
            _check_control_get_method("self", client, item)
            _check_control_get_method("profile", client, item)

    def test_post(self, client):
        pass


class TestPortfolioCurrency(object):
	""" Tests for PortfolioCurrency resource. """
	RESOURCE_URL = "/api/accounts/test-account-1/portfolio/pcurrencies/doge/"
	INVALID_URL = "/api/accounts/test-account-1/portfolio/pcurrencies/JOKUIHIME/"

	def test_get(self, client):
		resp = client.get(self.RESOURCE_URL)
		assert resp.status_code == 200
		body = json.loads(resp.data)
		_check_namespace(client, body)
		_check_control_get_method("profile", client, body)
		_check_control_get_method("collection", client, body)
		_check_control_get_method("crymo:currency-info", client, body)
		_check_control_delete_method("crymo:delete", client, body)


	def test_put(self, client):
		pass
	def test_delete(self, client):
		pass
