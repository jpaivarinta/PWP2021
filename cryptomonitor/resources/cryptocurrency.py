import json
from flask_restful import Resource
from flask_restful import Api
from flask import Response, url_for
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.models import CryptoCurrency
from cryptomonitor.constants import *

""" 
Source and help from
https://github.com/enkwolf/pwp-course-sensorhub-api-example and
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

class CryptoCurrencyItem(Resource):

    def get(self, currency):
        """
        GET method for getting single cryptocurrency
        """
        currencyitem = CryptoCurrency.query.filter_by(abbreviation=currency.upper()).first()
        if currencyitem is None:
            return create_error_response(404, "Currency not in database")

        body = CryptoMonitorBuilder(
            name=currencyitem.name,
            abbreviation=currencyitem.abbreviation,
            timestamp=currencyitem.timestamp,
            value=currencyitem.value,
            daily_growth=currencyitem.daily_growth
        )

        body.add_namespace("crymo", LINK_RELATIONS_URL)
        body.add_control("self", url_for("api.cryptocurrencyitem", currency=currencyitem.abbreviation))
        body.add_control_all_currencies()
        body.add_control_all_accounts()
        body.add_control("profile", CCURRENCY_PROFILE)
        return Response(json.dumps(body, default=str), 200, mimetype=MASON)

class CryptoCurrencyCollection(Resource):

    def get(self):
        """
        GET method for getting all cryptocurrencies known by API
        """
        body = CryptoMonitorBuilder(items=[])

        body.add_namespace("crymo", LINK_RELATIONS_URL)
        body.add_control("self", "/api/currencies/")
        body.add_control_all_accounts()
        body.add_control("profile", CCURRENCY_PROFILE)

        for currency in CryptoCurrency.query.all():
            item = CryptoMonitorBuilder(
                name=currency.name,
                abbreviation=currency.abbreviation,
                timestamp=currency.timestamp,
                value=currency.value,
                daily_growth=currency.daily_growth
            )
            item.add_control("self", url_for("api.cryptocurrencyitem", currency=currency.abbreviation ))
            item.add_control("profile", CCURRENCY_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body, default=str), 200, mimetype=MASON)
