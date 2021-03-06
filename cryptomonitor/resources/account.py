import json
from jsonschema import validate, ValidationError
from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from cryptomonitor.models import UserAccount, Portfolio, crypto_portfolio
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.constants import *
from cryptomonitor import db
from datetime import datetime

""" 
Source and help from
https://github.com/enkwolf/pwp-course-sensorhub-api-example and
https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

class AccountCollection(Resource):

    def get(self):
        """
        GET method for getting all accounts
        """
        body = CryptoMonitorBuilder(items = [])
        for single_account in UserAccount.query.all():
            item =  CryptoMonitorBuilder(     
                id=single_account.id,
                name=single_account.name,
                password=single_account.password,
                portfolio_id=single_account.portfolio_id
            )
            item.add_control("self", url_for("api.accountitem", account=single_account.name))
            item.add_control("profile", ACCOUNT_PROFILE)
            item.add_control("portfolio", url_for("api.portfolioitem", account=single_account.name))
            body["items"].append(item)


        body.add_control_add_account()
        body.add_control("self", url_for("api.accountcollection"))
        body.add_namespace("crymo", LINK_RELATIONS_URL)

        #Returning list of all accounts
        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )

    def post(self):
        """
        POST method for adding a new account
        """
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Request must be JSON"
            )
        try:
            validate(request.json, UserAccount.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        try:
            useraccount = UserAccount(
                name=request.json["name"],
                password=request.json["password"],
            )
            pf = Portfolio(
                timestamp=datetime.now(),
                value=0.0
            )
            useraccount.portfolio = pf
            db.session.add(useraccount)
            db.session.add(pf)
            db.session.commit()

        except IntegrityError:
            return create_error_response(409, "Already exists",
            "User account with name {} already exists".format(request.json["name"]))

        return Response(status=201, headers={
                "Location": url_for("api.accountitem", account=request.json["name"])
        })


class AccountItem(Resource):

    def get(self, account):
        """
        GET method for getting single account
        """
        single_account = UserAccount.query.filter_by(name=account).first()
        if single_account is None:
            return create_error_response(
                404, "Not found",
                "Account not found by name: {}".format(account)
            )

        body = CryptoMonitorBuilder(
            id=single_account.id,
            name=single_account.name,
            portfolio_id=single_account.portfolio_id,
            password=single_account.password
        )

        body.add_control("self", url_for("api.accountitem", account=account))
        body.add_control("profile", ACCOUNT_PROFILE) 
        body.add_control("portfolio", href=url_for("api.portfolioitem", account=single_account.name))
        body.add_control_all_accounts()
        body.add_control_edit_account(account=account)
        body.add_control_delete_account(account=account)
        body.add_namespace("crymo", LINK_RELATIONS_URL)

        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def put(self, account):
        """
        PUT method for editing account resource
        """
        single_account = UserAccount.query.filter_by(name=account).first()
        if single_account is None:
            return create_error_response(
                404, "Not found",
                "Account not found by name: {}".format(account)
            )
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Request content type must be JSON"
            )

        try:
            validate(request.json, UserAccount.get_schema())
        except ValidationError as e:
            return create_error_response(
                400, "Invalid JSON document",
                str(e)
            )

        single_account.name = request.json["name"]
        single_account.password = request.json["password"]

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return create_error_response(
                409, "Already exists",
                "Account with given name already exists"
            )

        return Response(
            status=204,
            mimetype=MASON
        )


    def delete(self, account):
        """
        DELETE method for deleting single account
        """
        single_account = UserAccount.query.filter_by(name=account).first()
        if single_account is None:
            return create_error_response(
                404, "Not found",
                "Account not found by name {}".format(account)
            )
        db.session.delete(single_account)
        db.session.commit()

        return Response(status=204, mimetype=MASON)