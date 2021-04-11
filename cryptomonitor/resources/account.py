import json
from jsonschema import validate, ValidationError
from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from cryptomonitor.models import UserAccount
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.constants import *
from cryptomonitor import db

class AccountCollection(Resource):
    def get(self):
        
        if request.method != 'GET':
            return "GET method required", 405

        body = CryptoMonitorBuilder(items = [])
        for single_account in UserAccount.query.all():
            item =  CryptoMonitorBuilder(
                id=single_account.id,
                name=single_account.name,
                portfolio_id=single_account.portfolio_id
            )
            item.add_control("self", url_for("api.accountitem", id=single_account.id)) #IS url correct?
            item.add_control("profile", ACCOUNT_PROFILE)
            body["items"].append(item)


        body.add_control_add_account()
        body.add_control("self", url_for("api.accounts"))                               #IS url correct?
        body.add_namespace("crymo", LINK_RELATIONS_URL)

        #Returning list of all accounts
        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )

    def post(self):
        if not request.json:
            return create_error_response(
                415, "Unsupported media type",
                "Request must be JSON"
            )
        try:
            validate(request.json, UserAccount.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        useraccount = UserAccount(
            name=request.json["name"],
            password=request.json["password"]
        )

        try:
            db.session.add(useraccount)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists",
            "User account with name {} already exists".format(request.json["name"]))

        return Response(status=201, headers={
                "Location": url_for("api.accountitem", useraccount=request.json["name"])
        })


class AccountItem(Resource):

    def get(self, account_name):
        single_account = UserAccount.query.filter_by(name=account_name).first()
        if single_account is None:
            return create_error_response(
                404, "Not found",
                "Account not found by name: {}".format(account_name)
            )

        body = CryptoMonitorBuilder(
            id=single_account.id,
            name=single_account.name,
            portfolio_id=single_account.portfolio_id
        )

        body.add_control("self", url_for("api.accountitem", account_name=account_name))
        body.add_control("profile", ACCOUNT_PROFILE) 
        body.add_control("portfolio", url_for("api.portfolioitem"), id=single_account.portfolio_id)
        body.add_control_all_accounts()
        body.add_control_edit_account(account_name=account_name)
        body.add_control_delete_account(account_name=account_name)
        body.add_namespace("crymo", LINK_RELATIONS_URL)

        return Response(response=json.dumps(body), status=200, mimetype=MASON)

    def put(self, account_name):
        """
        PUT method for editing account resource
        """
        single_account = UserAccount.query.filter_by(name=account_name).first()
        if single_account is None:
            return create_error_response(
                404, "Not found",
                "Account not found by name: {}".format(account_name)
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
            deb.session.rollback()
            return create_error_response(
                409, "Already exists",
                "Account with given name already exists"
            )

        return Response(
            status=204,
            mimetype=MASON
        )


    def delete(self, account_name):
        single_account = UserAccount.query.filter_by(name=account_name).first()
        if single_account is None:
            return create_error_response(
                404, "Not found",
                "Account not found by name {}".format(account_name)
            )
        db.session.delete(single_account)
        db.session.commit()

        return Response(204, mimetype=MASON)