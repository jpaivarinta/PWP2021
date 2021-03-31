import json
from flask_restful import Resource
from flask_restful import Api
from flask import Response
from ..api import api
from ..utils import CryptoMonitorBuilder
from ..utils import create_error_response
from ..models import UserAccount, Portfolio, CryptoCurrency, crypto_portfolio

MASON = "application/vnd.mason+json"
PROFILE = "profiles/portfolio"

class PortfolioItem(Resource):
    def get(self, username):
        db_user = UserAccount.query.filter_by(name=username).first()
        if db_user is None:
            return create_error_response(404, "User not found", "User doesn't exist, so portfolio cannot be returned")
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        """portfolio_currencies = CryptoMonitorBuilder(items=[])
        for portfolio_currency in crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id):
            cryptocurrency = CryptoCurrency.query.filter_by(id=portfolio_currency.cryptocurrency_id).first()
            item = CryptoMonitorBuilder(
                name=cryptocurrency.name,
                currencyAmount=portfolio_currency.currencyAmount
            )
            portfolio_currencies["items"].append(item)"""
        body = CryptoMonitorBuilder(timestamp=db_portfolio.timestamp,
                                    value=db_portfolio.value)
        body.add_namespace("crymo", "/cryptometa/link-relations#")
        body.add_control("self", api.url_for(Portfolio, id=db_portfolio.id))
        body.add_control("up", api.url_for(UserAccount, name=username))
        body.add_control_pcurrencies_all()
        return Response(json.dumps(body), 200, mimetype=MASON)
