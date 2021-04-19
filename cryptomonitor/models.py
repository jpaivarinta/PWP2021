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

# cryptoPortfolio = db.Table("cryptoPortfolio",
#     db.Column("cryptocurrency_id", db.Integer, db.ForeignKey("cryptocurrency.id"), primary_key=True),
#     db.Column("portfolio_id", db.Integer, db.ForeignKey("portfolio.id"), primary_key=True),
#     db.Column("amount", db.Float)
# )

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
            "type": "string"
        }
        return schema

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) #is this necessary?
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"))

    portfolio = db.relationship("Portfolio", back_populates="useraccount", uselist=False)

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
    value = db.Column(db.Float, nullable=False) #How to accept only positive?
    # useraccount_id = db.Column(db.Integer, db.ForeignKey("user_account.id"))

    cryptocurrencies = db.relationship("crypto_portfolio",  back_populates="portfolio")
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

    a1 = UserAccount(
        name="test-account-1",
        password="pswd"
    )

    a2 = UserAccount(
        name="test-account-2",
        password="pswd"
    )

    p1 = Portfolio(
        timestamp=datetime.now(),
        value=100.0
    )

    p2 = Portfolio(
        timestamp=datetime.now(),
        value=200.0
    )

    a1.portfolio = p1
    a2.portfolio = p2

    c1 = CryptoCurrency(
        name = "Bitcoin",
        abbreviation = "BTC",
        timestamp = datetime.now(),
        value = 50000.0,
        daily_growth = 2.5
    )
    c2 = CryptoCurrency(
        name = "Ethereum",
        abbreviation = "ETH",
        timestamp = datetime.now(),
        value = 1700.0,
        daily_growth = 5.5
    )

    cp1 = crypto_portfolio(
        currencyAmount=5.5,
        cryptocurrency=c1,
        portfolio=p1
    )

    cp2 = crypto_portfolio(
        currencyAmount=6.5,
        cryptocurrency=c2,
        portfolio=p2
    )

    db.session.add(a1)
    db.session.add(a2)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(cp1)
    db.session.add(cp2)
    db.session.commit()