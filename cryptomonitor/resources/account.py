import json
from jsonschema import validate, ValidationError
from flask import request, Response, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from cryptomonitor.models import UserAccount
from cryptomonitor.utils import CryptoMonitorBuilder, create_error_response
from cryptomonitor.constants import *

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
    def get(self, name):
        pass
    def put(self, name):
        pass
    def delete(self,name):
        pass

