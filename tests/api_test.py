import json
import os
import tempfile
from datetime import datetime

import pytest
from cryptomonitor import create_app, db
from cryptomonitor.models import UserAccount, Portfolio, CryptoCurrency, crypto_portfolio
from jsonschema import validate
from sqlalchemy import event
from sqlalchemy.engine import Engine

""" 
Source and help from
https://github.com/enkwolf/pwp-course-sensorhub-api-example and
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""


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
			name="test-account-{}".format(i),
			password="testpwd"
		)
		p = Portfolio(
			timestamp=datetime.now(),
			value=float(i * 100)
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
	"""
	Get a valid portfoliocurrency object
	Args:
		name: Abbreviation of the cryptocurrency
		amount: Amount of cryptocurrencies

	Returns:
	Portfoliocurrency object
	"""
	return {"currencyname": "{}".format(name), "currencyamount": "{}".format(amount)}


def _get_account_json(name, password):
	"""
	Get valid account object.
	Args:
		name: Name of the account
		password: Password of the account

	Returns:
	Account object
	"""
	return {"name": "{}".format(name), "password": "{}".format(password)}


def _get_CryptoCurrency():
	return CryptoCurrency(
		name="DogeCoin",
		abbreviation="DOGE",
		timestamp=datetime.now(),
		value=0.0462,
		daily_growth=7.1,
		launchDate=datetime(2012, 5, 12),
		blockchain_length=3610463
	)


def _get_CryptoCurrency2():
	return CryptoCurrency(
		name="Bitcoin",
		abbreviation="BTC",
		timestamp=datetime.now(),
		value=50000.00,
		daily_growth=7.1,
		launchDate=datetime(2012, 5, 12),
		blockchain_length=3610463
	)


def _get_CryptoCurrency3():
	return CryptoCurrency(
		name="Litecoin",
		abbreviation="LTC",
		timestamp=datetime.now(),
		value=10000.00,
		daily_growth=2.1,
		launchDate=datetime(1500, 5, 12),
		blockchain_length=3610463
	)


# GENERAL CONTROL CHECKS

def _check_namespace(client, response):
	"""
	Checks that the "crymo" namespace is found from the response body, and
	that its "name" attribute is a URL that can be accessed.
	"""
	ns_href = response["@namespaces"]["crymo"]["name"]
	resp = client.get(ns_href)
	assert resp.status_code == 200


def _check_control_get_method(ctrl, client, obj):
	"""
	Checks a GET type control from a JSON object be it root document or an item
	in a collection. Also checks that the URL of the control can be accessed.
	"""
	href = obj["@controls"][ctrl]["href"]
	resp = client.get(href)
	assert resp.status_code == 200


def _check_control_delete_method(ctrl, client, obj):
	"""
	Checks a DELETE type control from a JSON object be it root document or an
	item in a collection. Checks the contrl's method in addition to its "href".
	Also checks that using the control results in the correct status code of 204.
	"""

	href = obj["@controls"][ctrl]["href"]
	method = obj["@controls"][ctrl]["method"].lower()
	assert method == "delete"
	resp = client.delete(href)
	assert resp.status_code == 204


# ACCOUNT CONTROL CHECKS

def _check_control_put_method_account(ctrl, client, obj):
	"""
	Checks a PUT type control from a JSON object be it root document or an item
	in a collection. In addition to checking the "href" attribute, also checks
	that method, encoding and schema can be found from the control. Also
	validates a valid game against the schema of the control to ensure that
	they match. Finally checks that using the control results in the correct
	status code of 204.
	"""

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
	"""
	Checks a POST type control from a JSON object be it root document or an item
	in a collection. In addition to checking the "href" attribute, also checks
	that method, encoding and schema can be found from the control. Also
	validates a valid sensor against the schema of the control to ensure that
	they match. Finally checks that using the control results in the correct
	status code of 201.
	"""

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
	"""
	Checks a PUT type control from a JSON object be it root document or an item
	in a collection. In addition to checking the "href" attribute, also checks
	that method, encoding and schema can be found from the control. Also
	validates a valid game against the schema of the control to ensure that
	they match. Finally checks that using the control results in the correct
	status code of 204.
	"""

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
	"""
	Checks a POST type control from a JSON object be it root document or an item
	in a collection. In addition to checking the "href" attribute, also checks
	that method, encoding and schema can be found from the control. Also
	validates a valid sensor against the schema of the control to ensure that
	they match. Finally checks that using the control results in the correct
	status code of 201.
	"""

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


class TestAccountCollection(object):
	""" Tests for AccountCollection resource. """
	RESOURCE_URL = "/api/accounts/"

	def test_get(self, client):
		""" Tests for GET method of AccountCollection resource. """
		resp = client.get(self.RESOURCE_URL)
		assert resp.status_code == 200
		body = json.loads(resp.data)
		_check_namespace(client, body)
		_check_control_post_method_account("crymo:add-account", client, body)
		assert len(body["items"]) == 3
		for item in body["items"]:
			_check_control_get_method("self", client, item)
			_check_control_get_method("profile", client, item)
			_check_control_get_method("portfolio", client, item)

	def test_post(self, client):
		""" Tests for POST method of AccountCollection resource. """
		valid = _get_account_json("juu", "testpwd")

		# test with wrong content type
		resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
		assert resp.status_code == 415

		# Test with valid and see if exists afterwards
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
		""" Tests for PUT method of AccountItem resource. """
		valid = _get_account_json("pekka", "testpwd")

		# Test with wrong content type
		resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
		assert resp.status_code == 415

		# Test with another account's name
		valid["name"] = "test-account-2"
		resp = client.put(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 409

		# Test with valid
		valid["name"] = "test-account-1"
		resp = client.put(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 204

		# Remove account for 400
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
		""" Tests for GET method of CryptoCurrencyCollection resource. """
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
	""" Test cryptocurrencycollection resource"""

	RESOURCE_URL = "/api/accounts/test-account-1/portfolio/"
	INVALID_URL = "/api/accounts/jorma/portfolio/"

	def test_get(self, client):
		resp = client.get(self.RESOURCE_URL)
		print(resp)
		assert resp.status_code == 200
		body = json.loads(resp.data)
		_check_namespace(client, body)
		for control in body["@controls"]:
			_check_control_get_method(control, client, body)

		resp = client.get(self.INVALID_URL)
		assert resp.status_code == 404


class TestPortfolioCurrencyCollection(object):
	""" Test portfoliocurrencycollection resource """

	RESOURCE_URL = "/api/accounts/test-account-1/portfolio/pcurrencies/"

	def test_get(self, client):
		resp = client.get(self.RESOURCE_URL)
		assert resp.status_code == 200
		body = json.loads(resp.data)
		_check_namespace(client, body)
		_check_control_post_method_pcurrency("crymo:add-pcurrency", client, body)
		assert len(body["items"]) == 2
		for item in body["items"]:
			_check_control_get_method("self", client, item)
			_check_control_get_method("profile", client, item)

	def test_post(self, client):
		valid = _get_pcurrency_json("LTC", "666.666")
		# test with wrong content type
		resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
		assert resp.status_code == 415

		# Test with valid and see if exists afterwards
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 201
		resp = client.get(resp.headers["Location"])
		assert resp.status_code == 200

		# send same data again for 409
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 409

		# remove model field for 400
		valid.pop("currencyname")
		resp = client.post(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 400


class TestPortfolioCurrency(object):
	""" Tests for PortfolioCurrency resource. """
	RESOURCE_URL = "/api/accounts/test-account-1/portfolio/pcurrencies/DOGE/"
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
		resp = client.get(self.INVALID_URL)
		assert resp.status_code == 404

	def test_put(self, client):
		""" Tests for PUT method of PortfolioCurrency resource. """
		valid = _get_pcurrency_json("LTC", "200.0")

		# Test with wrong content type
		resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
		assert resp.status_code == 415

		# Test with non existent cryptocurrency
		resp = client.put(self.INVALID_URL, json=valid)
		assert resp.status_code == 404

		# test with valid currencyname
		resp = client.put(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 204

		# Test with negative currencyamount 400
		valid["currencyamount"] = str(-222.4)
		resp = client.put(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 400


		# Test for invalid json 400
		valid.pop("currencyname")
		resp = client.put(self.RESOURCE_URL, json=valid)
		assert resp.status_code == 400

	def test_delete(self, client):
		""" Tests for DELETE method of PortfolioCurrency resource. """
		resp = client.delete(self.RESOURCE_URL)
		assert resp.status_code == 204
		resp = client.delete(self.RESOURCE_URL)
		assert resp.status_code == 404
		resp = client.delete(self.RESOURCE_URL)
		assert resp.status_code == 404
