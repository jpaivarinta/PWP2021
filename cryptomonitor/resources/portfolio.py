import json
from flask_restful import Resource
from flask import Response, url_for

from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.models import UserAccount, Portfolio
from cryptomonitor.constants import *

""" 
Source and help from
https://github.com/enkwolf/pwp-course-sensorhub-api-example and
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

class PortfolioItem(Resource):

    def get(self, account):
        """
        GET method for getting portfolio
        """
        db_user = UserAccount.query.filter_by(name=account).first()
        if db_user is None:
            return create_error_response(
                404,
                "Account doesn't exist"
            )
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        body = CryptoMonitorBuilder(timestamp=db_portfolio.timestamp.isoformat(), value=db_portfolio.value)
        
        body.add_namespace("crymo", LINK_RELATIONS_URL)
        body.add_control("self", href=url_for("api.portfolioitem", account=db_user.name))
        body.add_control("up", href=url_for("api.accountitem", account=db_user.name))
        body.add_control_all_pcurrencies(db_user.name)
        body.add_control("profile", PORTFOLIO_PROFILE)
        return Response(response=json.dumps(body), status=200, mimetype=MASON)
