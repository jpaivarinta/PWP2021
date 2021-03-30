from flask_restful import Resource, Api
from flask import request, Response
from ..cryptodb import UserAccount
from ..utils import CryptoMonitorBuilder, create_error_response


class Accounts(Resource):
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

        """
            Add control stuff here
        """



        """
            Returning list of all useraccounts.
        """
        return Response(
            status=200,
            response=json.dumps(body),
            mimetype=MASON
        )


    def post(self):
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Request must be JSON")

class Account(Resource):
    def get(self, name):
        pass
    def put(self, name):
        pass
    def delete(self,name):
        pass

