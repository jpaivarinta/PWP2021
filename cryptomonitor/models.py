from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
        pass

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