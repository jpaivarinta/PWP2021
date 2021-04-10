from flask import Blueprint
from flask_restful import Api

from cryptomonitor.resources.account import AccountCollection, AccountItem
from cryptomonitor.resources.cryptocurrency import CryptoCurrencyItem, CryptoCurrencyCollection
from cryptomonitor.resources.portfolio import PortfolioItem
from cryptomonitor.resources.portfoliocurrency import PortfolioCurrency, PortfolioCurrencyCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

"""api.add_resource(AccountCollection, "/accounts/")
api.add_resource(AccountItem, "/accounts/<account>/")
api.add_resource(CryptoCurrencyItem, "/currencies/<currency>/")
api.add_resource(CryptoCurrencyCollection, "/currencies/")
api.add_resource(PortfolioItem, "/accounts/<account>/portfolio/")
api.add_resource(PortfolioCurrency, "/accounts/<account>/portfolio/pcurrencies/<pcurrency>")
api.add_resource(PortfolioCurrencyCollection, "/accounts/<account>/pcurrencies/")"""
