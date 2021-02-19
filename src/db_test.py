import pytest
from datetime import datetime
import tempfile
import os
import app

from database.cryptodb import db, UserAccount, Portfolio, CryptoCurrency, crypto_portfolio
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



@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()

    test_app = app.app
    test_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    test_app.config["TESTING"] = True
    db.init_app(test_app)

    with test_app.app_context():
        db.create_all()

        yield db

    db.session.remove()
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
    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=cryptoCurrency, currencyAmount=44.444)
    portfolio.cryptocurrencies.append(cp)

    db_handle.session.add(userAccount)
    db_handle.session.add(portfolio)
    db_handle.session.add(cryptoCurrency)

    db_handle.session.add(cp)
    db_handle.session.commit()

    # Check existence
    assert UserAccount.query.count() == 1
    assert Portfolio.query.count() == 1
    assert CryptoCurrency.query.count() == 1
    assert crypto_portfolio.query.count() == 1

    db_user = UserAccount.query.first()
    db_portfolio = Portfolio.query.first()
    db_cryptocurreny = CryptoCurrency.query.first()
    db_cp = crypto_portfolio.query.first()

    # check Relationships
    assert db_user.portfolio == db_portfolio
    assert db_user in db_portfolio.useraccount
    assert db_portfolio == db_cp.portfolio
    assert db_cryptocurreny == db_cp.cryptocurrency  