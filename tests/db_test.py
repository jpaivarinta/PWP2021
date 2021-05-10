import pytest
from datetime import datetime
import tempfile
import os
from cryptomonitor import create_app, db
from cryptomonitor.models import UserAccount, Portfolio, CryptoCurrency, crypto_portfolio
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

""" 
Source and help from
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""


"""
*** DATABASE TESTS ***
"""


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()

    test_app = create_app()
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


def _get_UserAccount2():
    return UserAccount(
        name="test_user2",
        password="asdfg",
    )


def _get_Portfolio2():
    return Portfolio(
        timestamp=datetime.now(),
        value=1234.56
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


def test_instance_creation(db_handle):
    """
    Test for instance creation, their existence, and relationships.
    """
    userAccount = _get_UserAccount()
    portfolio = _get_Portfolio()
    cryptoCurrency = _get_CryptoCurrency()
    userAccount.portfolio = portfolio
    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=cryptoCurrency, currencyAmount=44.444)

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
    assert db_user == db_portfolio.useraccount
    assert db_portfolio == db_cp.portfolio
    assert db_cryptocurreny == db_cp.cryptocurrency


def test_cryptoportfolio_currency_one(db_handle):
    """
    Test if the same currency cannot be added twice to the same portfolio.
    """
    usr = _get_UserAccount()
    portfolio = _get_Portfolio()
    currency = _get_CryptoCurrency()

    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)
    cp2 = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)
    usr.portfolio = portfolio
    db_handle.session.add(usr)
    db_handle.session.add(portfolio)
    db_handle.session.add(currency)
    db_handle.session.add(cp)

    with pytest.raises(IntegrityError):
        db_handle.session.commit()


def test_addSecondCurrencyToPortfolio(db_handle):
    """
    Test if another cryptocurrency can be added to portfolio.
    """
    usr = _get_UserAccount()
    portfolio = _get_Portfolio()
    currency = _get_CryptoCurrency()
    currency2 = _get_CryptoCurrency2()

    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)
    cp2 = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency2, currencyAmount=44.444)
    usr.portfolio = portfolio

    db_handle.session.add(usr)
    db_handle.session.add(portfolio)
    db_handle.session.add(currency)
    db_handle.session.add(cp)
    db_handle.session.add(cp2)

    db_handle.session.commit()

    db_portfolio = Portfolio.query.first()
    assert crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).count()==2

def test_removeCurrencyFromPortfolio(db_handle):
    """
    Test if a currency can be removed from portfolio.
    """
    usr = _get_UserAccount()
    portfolio = _get_Portfolio()
    currency = _get_CryptoCurrency()
    currency2 = _get_CryptoCurrency2()

    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)
    cp2 = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency2, currencyAmount=44.444)
    usr.portfolio = portfolio

    db_handle.session.add(usr)
    db_handle.session.add(portfolio)
    db_handle.session.add(currency)
    db_handle.session.add(cp)
    db_handle.session.commit()

    db_portfolio = Portfolio.query.first()
    assert crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).count()==2

    db_currency = CryptoCurrency.query.filter_by(abbreviation="BTC").first()
    db_cp = crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id, cryptocurrency_id=db_currency.id).first()
    db_handle.session.delete(db_cp)
    db_handle.session.commit()

    assert crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).count()==1
  

def test_get_portfolios_by_currency(db_handle):
  """ 
  Test getting portfolios having certain cryptocurrency
  """
  usr = _get_UserAccount()
  usr2 = _get_UserAccount2()

  portfolio = _get_Portfolio()
  portfolio2 = _get_Portfolio2()

  currency = _get_CryptoCurrency()
  
  
  cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)
  cp2 = crypto_portfolio(portfolio=portfolio2, cryptocurrency=currency, currencyAmount=20.444)

  usr.portfolio = portfolio
  usr2.portfolio = portfolio2

  db_handle.session.add(usr)
  db_handle.session.add(usr2)

  db_handle.session.add(portfolio)
  db_handle.session.add(portfolio2)

  db_handle.session.add(currency)
  db_handle.session.add(cp)
  db_handle.session.add(cp2)

  db_handle.session.commit()

  db_currency = CryptoCurrency.query.first()

  assert crypto_portfolio.query.filter_by(cryptocurrency_id=db_currency.id).count()==2

def test_update_currencyamount(db_handle):
    """ 
    Test updating currency amount in portfolio
    NOTE: might be redundant test
    """
    usr = _get_UserAccount()

    portfolio = _get_Portfolio()

    currency = _get_CryptoCurrency()

    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)

    usr.portfolio = portfolio

    db_handle.session.add(usr)

    db_handle.session.add(portfolio)

    db_handle.session.add(currency)
    db_handle.session.add(cp)

    db_handle.session.commit()

    # update user's portfolio's certain currencyamount
    db_user = UserAccount.query.first()
    db_currency = CryptoCurrency.query.first()
    db_cp = crypto_portfolio.query.filter_by(portfolio_id=db_user.portfolio.id, cryptocurrency_id=db_currency.id).first()

    assert db_cp.currencyAmount == 44.444

    db_cp.currencyAmount=2
    db_handle.session.commit()

    assert db_cp.currencyAmount == 2

def test_delete_user(db_handle):
    """ 
    Test deleting user, portfolio, bulkdeleting crypto_portfolios
    NOTE: might be redundant test
    """
    usr = _get_UserAccount()

    portfolio = _get_Portfolio()
    portfolio2 = _get_Portfolio2()

    currency = _get_CryptoCurrency()
    currency2 = _get_CryptoCurrency2()

    cp = crypto_portfolio(portfolio=portfolio, cryptocurrency=currency, currencyAmount=44.444)
    cp2 = crypto_portfolio(portfolio=portfolio,cryptocurrency=currency2, currencyAmount=400.0)
    cp3 = crypto_portfolio(portfolio=portfolio2, cryptocurrency=currency, currencyAmount=9.0)

    usr.portfolio = portfolio

    db_handle.session.add(usr)

    db_handle.session.add(portfolio)

    db_handle.session.add(currency)
    db_handle.session.add(currency2)
    db_handle.session.add(cp)
    db_handle.session.add(cp2)
    db_handle.session.add(cp3)

    db_handle.session.commit()

    assert crypto_portfolio.query.count()==3

    db_user = UserAccount.query.first()
    db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
    bulk_delete_query = crypto_portfolio.__table__.delete().where(crypto_portfolio.portfolio_id==db_portfolio.id)
    db_handle.session.execute(bulk_delete_query)
    db_handle.session.delete(db_portfolio) 
    db_handle.session.delete(db_user)
    db_handle.session.commit()

    assert crypto_portfolio.query.count() == 1
