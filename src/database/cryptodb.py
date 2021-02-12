from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cpdata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

cryptoPortfolio = db.Table("cryptoPortfolio",
    db.Column("cryptocurrency_id", db.Integer, db.ForeignKey("cryptocurrency.id"), primary_key=True),
    db.Column("portfolio_id", db.Integer, db.ForeignKey("portfolio.id"), primary_key=True)
)

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) #is this necessary?
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"))

    portfolio = db.relationship("Portfolio", back_populates="useraccount")
    pass

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False) #How to accept only positive?

    cryptocurrencies = db.relationship("Cryptocurrency", secondary=cryptoPortfolio, back_populates="portfolios")
    useraccount = db.relationship("UserAccount", back_populates="portfolio")

    pass

class CryptoCurrency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    abbreviation = db.Column(db.String(12), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float, nullable=False) #How to accept only positive?
    daily_growth = db.Column(db.Float, nullable=False)
    launchDate = db.Column(db.DateTime)
    blockchain_length = db.Column(db.Float)

    portfolios = db.relationship("Portfolio", secondary=cryptoPortfolio, back_populates="cryptocurrencies")
    pass