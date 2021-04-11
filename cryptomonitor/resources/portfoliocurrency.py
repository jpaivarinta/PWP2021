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
        # if user is None:
        #     return create_error_response(404, "User not found")
        port = Portfolio.query.filter_by(id=user.portfolio_id).first()

        currency = CryptoCurrency.query.filter_by(abbreviation=currencyname).first()
        # if currency is None:
        #     return create_error_response(404, "Currency not found in system")
        
        pcurrencies = crypto_portfolio.query.filter_by(portfolio_id=port.id).all()
        for pc in pcurrencies:
            if pc.cryptocurrency_id==currency.id:
                pcurrency = pc
                break
        if pcurrency:
            body = CryptoMonitorBuilder(id=currency.id, name=currency.name, abbreviation=currency.abbreviation,
            timestamp=currency.timestamp, value=currency.value, daily_growth=currency.daily_growth,
            launchDate=currency.launchDate, blockchain_length=currency.blockhain_length, currencyAmount=pc.currencyAmount 
            )  
            body.add_namespace("crymo", LINK_RELATIONS_URL)
            body.add_control("self", url_for("api.portfoliocurrency", username, currencyname))
            body.add_control("profile", PCURRENCY_PROFILE)
            body.add_control("collection", url_for("api.portfoliocurrencycollection"))
            body.add_control_get_currency_info(currency.abbreviation)
            body.add_control_edit_pcurrency(username, currencyname)
            body.add_control_delete_pcurrency(username, currencyname)
            return Response(json.dumps(body), 200, mimetype=MASON)
        else:
            return create_error_response(404, "Currency not found in portfolio")



    def put(self, username):

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Request body must be json")
        try:
            validate(request.json, crypto_portfolio.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid json body")
        # Get the user's portfolio
        db_user = UserAccount.query.filter_by(name=username).first()
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        # Get the cryptocurrency
        db_currency = CryptoCurrency.query.filter_by(abbrevation=request.json["currencyname"]).first()

        # Find the pcurrency from users portfolio 
        db_pcurrencies = crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).all()
        for pc in db_pcurrencies:
             if pc.cryptocurrency_id==db_currency.id:
                 pcurrency = pc
                 break
        if pcurrency:
            pcurrency.currencyAmount = request.json["currencyamount"]
            db.session.commit()
        else:
            return create_error_response(404, "Currency not in portfolio")
        return Response(status=204)

    def delete(self, username, currencyname):
        """
        Remoove pcurrency from the user's portfolio 
        """
        # Get the user's portfolio
        db_user = UserAccount.query.filter_by(name=username).first()
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        # Get the cryptocurrency
        db_currency = CryptoCurrency.query.filter_by(abbrevation=currencyname).first()

        # Find the pcurrency from users portfolio 
        db_pcurrencies = crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).all()
        for pc in db_pcurrencies:
            if pc.cryptocurrency_id==db_currency.id:
                db.session.delete(pc)
                db.session.commit()
                return Response(status=204)
        return create_error_response(404, "Currency not found in user's portfolio")

class PortfolioCurrencyCollection(Resource):
    def get(self, username):
        """ 
        Get user's portfoliocurrency collection
        """
        # Get user
        db_user = UserAccount.query.filter_by(name=username).first()

        if db_user is None:
            return create_error_response(404, "User not found")
        # Get user's portfolio
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        # Get portfoliocurrencies
        db_pcurrencies = crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).all()

        body = CryptoMonitorBuilder(
            items = []
        )
        body.add_namespace("crymo", LINK_RELATIONS_URL)
        base_uri = url_for("api.portfoliocurrencycollection", username=username)
        body.add_control("up", url_for("api.portfolioitem", username=username))
        body.add_control("self", base_uri)
        body.add_control_add_pcurrency(username)

        for pc in db_pcurrencies:
            db_currency = CryptoCurrency.query.filter_by(id=pc.cryptocurrency_id).first()
            item = CryptoMonitorBuilder(
                currencyamount=pc.currencyAmount,
                currencyname=db_currency.abbreviation
            ) 
            body['items'].append(pc)
        return Response(json.dumps(body), 200, mimetype=MASON)


    def post(self, username):
        if not request.json:
            return create_error_response(415, "Unsupported media type")
        try:
            validate(request.json, crypto_portfolio.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid json document", str(e))

        db_user = UserAccount.query.filter_by(name=username).first()
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        db_currency = CryptoCurrency.query.filter_by(name=request.json["currencyname"]).first()
        if db_currency is None:
            return create_error_response(404, "Currency not found") 
        pcurrency = crypto_portfolio(
            portfolio=db_portfolio, 
            cryptocurrency=db_currency, 
            currencyAmount=request.json["currencyAmount"]
        )

        try:
            db.session.add(pcurrency)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists")

        return Response(status=201, headers={
            "Location": url_for("api.portfoliocurrency", username=username, currencyname=request.json["currencyname"])
        })

        