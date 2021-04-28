import json
from jsonschema import validate, ValidationError
from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from cryptomonitor.models import UserAccount, crypto_portfolio, Portfolio, CryptoCurrency
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.constants import *
from cryptomonitor import db

""" 
Source and help from
https://github.com/enkwolf/pwp-course-sensorhub-api-example and
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

class PortfolioCurrency(Resource):
    def get(self, account, pcurrency):
        user = UserAccount.query.filter_by(name=account).first()
        if user is None:
            return create_error_response(404, "User not found")
        port = Portfolio.query.filter_by(id=user.portfolio_id).first()

        currency = CryptoCurrency.query.filter_by(abbreviation=pcurrency).first()
        
        if currency is None:
            return create_error_response(404, "Currency not found in system")
        
        pcurrencies = crypto_portfolio.query.filter_by(portfolio_id=port.id).all()
        pfolio_currency = None
        for pc in pcurrencies:
            if pc.cryptocurrency_id==currency.id:
                pfolio_currency = pc
                break
        if pfolio_currency is not None:
            body = CryptoMonitorBuilder(id=currency.id, name=currency.name, abbreviation=currency.abbreviation,
            timestamp=currency.timestamp.isoformat(), value=currency.value, daily_growth=currency.daily_growth,
            launchDate=currency.launchDate.isoformat(), blockchain_length=currency.blockchain_length, currencyAmount=pc.currencyAmount 
            )  
            body.add_namespace("crymo", LINK_RELATIONS_URL)
            body.add_control("self", url_for("api.portfoliocurrency", account=account, pcurrency=pcurrency))
            body.add_control("profile", PCURRENCY_PROFILE)
            body.add_control("collection", url_for("api.portfoliocurrencycollection", account=account))
            body.add_control_get_currency_info(currency.abbreviation)
            body.add_control_edit_pcurrency(account=account, pcurrency=pcurrency)
            body.add_control_delete_pcurrency(account, currency.abbreviation)
            return Response(json.dumps(body), status=200, mimetype=MASON)
        else:
            return create_error_response(404, "Currency not found in portfolio")



    def put(self, account, pcurrency):

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Request body must be json")
        try:
            validate(request.json, crypto_portfolio.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid json body", str(e))

        if float(request.json["currencyamount"]) < 0:
            return create_error_response(400, "Invalid json body", "Currencyamount can't be negative")
        # Get the user's portfolio
        db_user = UserAccount.query.filter_by(name=account).first()
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        # Get the cryptocurrency
        db_currency = CryptoCurrency.query.filter_by(abbreviation=pcurrency.upper()).first()
        if db_currency is None:
            return create_error_response(404, "Currency doesn't exist")
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

    def delete(self, account, pcurrency):
        """
        Remove pcurrency from the user's portfolio 
        """
        # Get the user's portfolio
        db_user = UserAccount.query.filter_by(name=account).first()
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        # Get the cryptocurrency
        db_currency = CryptoCurrency.query.filter_by(abbreviation=pcurrency).first()
        
        # Find the pcurrency from users portfolio 
        db_pcurrencies = crypto_portfolio.query.filter_by(portfolio_id=db_portfolio.id).all()
        for pc in db_pcurrencies:
            if pc.cryptocurrency_id==db_currency.id:
                db.session.delete(pc)
                db.session.commit()
                return Response(status=204)
        return create_error_response(404, "Currency not found in user's portfolio")

class PortfolioCurrencyCollection(Resource):
    def get(self, account):
        """ 
        Get user's portfoliocurrency collection
        """
        # Get user
        db_user = UserAccount.query.filter_by(name=account).first()

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
        base_uri = url_for("api.portfoliocurrencycollection", account=account)
        body.add_control("up", url_for("api.portfolioitem", account=account))
        body.add_control("self", base_uri)
        body.add_control_add_pcurrency(account)

        for pc in db_pcurrencies:
            db_currency = CryptoCurrency.query.filter_by(id=pc.cryptocurrency_id).first()
            item = CryptoMonitorBuilder(
                currencyamount=pc.currencyAmount,
                currencyname=db_currency.abbreviation
            ) 
            item.add_control("self", url_for("api.portfoliocurrency", account=account, pcurrency=db_currency.abbreviation))
            item.add_control("profile", PCURRENCY_PROFILE)
            body['items'].append(item)
        return Response(json.dumps(body), status=200, mimetype=MASON)


    def post(self, account):
        if not request.json:
            return create_error_response(415, "Unsupported media type")
        try:
            validate(request.json, crypto_portfolio.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid json document", str(e))

        if float(request.json["currencyamount"]) <= 0:
            return create_error_response(400, "Invalid json document", "Currencyamount must be over zero")

        db_user = UserAccount.query.filter_by(name=account).first()
        db_portfolio = Portfolio.query.filter_by(id=db_user.portfolio_id).first()
        db_currency = CryptoCurrency.query.filter_by(abbreviation=request.json["currencyname"].upper()).first()
        if db_currency is None:
            return create_error_response(404, "Currency not found") 
        pcurrency = crypto_portfolio(
            portfolio=db_portfolio, 
            cryptocurrency=db_currency, 
            currencyAmount=request.json["currencyamount"]
        )

        try:
            db.session.add(pcurrency)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists")

        return Response(status=201, headers={
            "Location": url_for("api.portfoliocurrency", account=account, pcurrency=request.json["currencyname"])
        })

        