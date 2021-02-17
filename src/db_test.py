import pytest
from datetime import datetime
import tempfile
import os
import app

from database.cryptodb import db, UserAccount, Portfolio, CryptoCurrency
from sqlalchemy.engine import Engine
from sqlalchemy import event


"""
*** TESTING DATABASE ***

- an instance of each model can be created, and they can be found 
  from database afterward
- foreign key relationships are created correctly ondelete and onmodify 
  behaviors for foreign keys work as intended

A more thorough checklist would also include:
- test uniqueness of columns by trying to create objects that violate each 
  individual unique column
- test that columns have their nullable attribute set correctly
- test that column types and restrictions have been set correctly

"""

#db.create_all() 


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True

    with app.app.app_context():
    	app.db.create_all()

    yield app.db

    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


def _get_UserAccount():
	return UserAccount(
		name="test_user",
		password="passwd",
	)

def _get_Portfolio():
	return Portfolio(
		timestamp=datetime.now(),
		value=1234.56
	)
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

def test_instance_creation(db_handle):
	userAccount = _get_UserAccount()
	portfolio = _get_Portfolio()
	cryptoCurrency = _get_CryptoCurrency()
	userAccount.portfolio = portfolio
	portfolio.cryptocurrencies.append(cryptoCurrency)

	db.session.add(userAccount)
	db.session.add(portfolio)
	db.session.add(cryptoCurrency)
	db.session.commit()
