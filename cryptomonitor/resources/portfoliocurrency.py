import json
from jsonschema import validate, ValidationError
from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from cryptomonitor.models import UserAccount, crypto_portfolio, Portfolio, CryptoCurrency
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.constants import *

class PortfolioCurrency(Resource):
    def get(self,username, currencyname):
        user = UserAccount.query.filter_by(name=username).first()
        port = Portfolio.query.filter_by(id=user.portfolio_id).first()
        cp = crypto_portfolio.query.filter_by(portfolio_id=port.id).first()
        currency = CryptoCurrency.query.filter_by(id=cp.cryptocurrency_id).first()
        if currency:
            if currency.abbreviation==currencyname:
                body = CryptoMonitorBuilder(id=currency.id, name=currency.name, abbreviation=currency.abbreviation,
                timestamp=currency.timestamp, value=curreny.value, daily_growth=currency.daily_growth,
                launchDate=currency.launchDate, blockchain_length=currency.blockhain_length 
                )  
                body.add_namespace("crymo")
                body.add_control("self", api.url_for(PortfolioCurrency, username, currencyname))
                body.add_control("profile", PCURRENCY_PROFILE)
                body.add_control("collection", api.url_for(PortfolioCurrencyCollection))
                body.add_control_get_currency_info(currency.abbreviation)
                body.add_control_edit_pcurrency(username, currencyname)
                body.add_control_delete_pcurrency(username, currencyname)
                return Response(json.dumps(body), 200, mimetype=MASON)

    def put(self, username, currencyname, currencyamount):
        pass
    def delete(self, username, currencyname):
        pass

class PortfolioCurrencyCollection(Resource):
    def get(self, username):
        pass
    def post(self, username, currencyname, currencyamount):
        pass

