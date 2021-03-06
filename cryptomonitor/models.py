import click
from flask.cli import with_appcontext
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cryptomonitor import db

""" 
Source and help from
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

class crypto_portfolio(db.Model):
    cryptocurrency_id = db.Column( db.Integer, db.ForeignKey("cryptocurrency.id"), primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"), primary_key=True)
    currencyAmount = db.Column(db.Float, nullable=False)

    portfolio = db.relationship("Portfolio", back_populates="cryptocurrencies")
    cryptocurrency = db.relationship("CryptoCurrency", back_populates="portfolios")

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["currencyname", "currencyamount"]
        }
        props = schema["properties"] = {}
        props["currencyname"] = {
            "description": "Abbreviation of currency",
            "type": "string"
        }
        props["currencyamount"] = {
            "description": "Amount of currency",
            "type": "number"
        }
        return schema

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id")) #not needed?

    portfolio = db.relationship("Portfolio", back_populates="useraccount", single_parent=True, cascade="all, delete-orphan", uselist=False)

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["name", "password"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name of user",
            "type": "string"
        }
        props["password"] = {
            "description": "Password of account",
            "type": "string"
        }
        return schema

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False)
    # useraccount_id = db.Column(db.Integer, db.ForeignKey("user_account.id"))

    cryptocurrencies = db.relationship("crypto_portfolio",  back_populates="portfolio", single_parent=True, cascade="all, delete-orphan")
    useraccount = db.relationship("UserAccount", back_populates="portfolio", uselist=False)

    @staticmethod
    def get_schema():
        pass

class CryptoCurrency(db.Model):
    __tablename__ ="cryptocurrency"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    abbreviation = db.Column(db.String(12), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False) #How to accept only positive?
    daily_growth = db.Column(db.Float, nullable=False)
    launchDate = db.Column(db.DateTime)
    blockchain_length = db.Column(db.Float)

    portfolios = db.relationship("crypto_portfolio", back_populates="cryptocurrency")

    @staticmethod
    def get_schema():
        pass

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()

@click.command("testgen")
@with_appcontext
def generate_test_data():
    c1 = CryptoCurrency(
        name="Bitcoin",
        abbreviation="BTC",
        timestamp=datetime.now(),
        value=50000.00,
        daily_growth=7.1,
        launchDate=datetime(2012, 5, 12),
        blockchain_length=3610463
    )
    c2 = CryptoCurrency(
        name = "Ethereum",
        abbreviation = "ETH",
        timestamp = datetime.now(),
        value = 1700.0,
        daily_growth = 5.5,
        launchDate=datetime(1500, 5, 12),
        blockchain_length=3610463
    )
    c3 = CryptoCurrency(
        name = "Litecoin",
        abbreviation = "LTC",
        timestamp = datetime.now(),
        value = 250.0,
        daily_growth = 5.5,
        launchDate=datetime(1500, 5, 12),
        blockchain_length=3610463
    )

    c4 = CryptoCurrency(
        name="Tether",
        abbreviation="USDT",
        timestamp=datetime.now(),
        value=1.0,
        daily_growth=0.01,
        launchDate=datetime(1500, 5, 12),
        blockchain_length=9191911
    )

    c5 = CryptoCurrency(
        name="XRP",
        abbreviation="XRP",
        timestamp=datetime.now(),
        value=1.67,
        daily_growth=9.21,
        launchDate=datetime(1500, 5, 12),
        blockchain_length=52547
    )

    c6 = CryptoCurrency(
        name="Polkadot",
        abbreviation="DOT",
        timestamp=datetime.now(),
        value=40.37,
        daily_growth=4.26,
        launchDate=datetime(1500, 5, 12),
        blockchain_length=57843
    )

    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.add(c5)
    db.session.add(c6)
    db.session.commit()