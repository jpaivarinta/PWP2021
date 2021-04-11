import json
from flask_restful import Resource
from flask_restful import Api
from flask import Response, url_for
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.models import CryptoCurrency
from cryptomonitor.constants import *


class CryptoCurrencyItem(Resource):
    def get(self, name):
        currency = CryptoCurrency.query.filter_by(name=name).first()
        if currency is None:
            return create_error_response(404, "Currency not in database")

        body = CryptoMonitorBuilder(
            name=currency.name,
            abbreviation=currency.abbreviation,
            timestamp=currency.timestamp,
            value=currency.value,
            daily_growth=currency.daily_growth
        )

        body.add_namespace("crymo", "/cryptometa/link-relations#")
        body.add_control("self", url_for("api.cryptocurrencyitem", currency=currency.abbreviation))
        body.add_control_all_currencies()
        body.add_control_all_accounts()
        body.add_control("profile", CCURRENCY_PROFILE)
        return Response(json.dumps(body), 200, mimetype=MASON)

class CryptoCurrencyCollection(Resource):
    def get(self):
        body = CryptoMonitorBuilder(items=[])

        body.add_namespace("crymo", "/cryptometa/link-relations#")
        body.add_control("self", "/currencies/")
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
            item.add_control("self", url_for("api.cryptocurrencyitem", currency=currency. )
            item.add_control("profile", CCURRENCY_PROFILE)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=MASON)
