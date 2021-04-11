import json
from flask_restful import Resource
from flask import Response
from cryptomonitor.api import api
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.models import UserAccount, Portfolio
from cryptomonitor.constants import *


class PortfolioItem(Resource):
    def get(self, username):
        db_user = UserAccount.query.filter_by(name=username).first()
        if db_user is None:
            return create_error_response(
                404,
                "Account doesn't exist"
            )
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        body = CryptoMonitorBuilder(timestamp=db_portfolio.timestamp,
                                    value=db_portfolio.value)
        body.add_namespace("crymo", "/cryptometa/link-relations#")
        body.add_control("self", api.url_for(Portfolio, id=db_portfolio.id))
        body.add_control("up", api.url_for(UserAccount, id=db_user.id))
        body.add_control_all_pcurrencies(db_user.id)
        body.add_control("profile", PORTFOLIO_PROFILE)
        return Response(json.dumps(body), 200, mimetype=MASON)
