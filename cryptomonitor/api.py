from flask import Blueprint
from flask_restful import Api

from cryptomonitor.resources.account import AccountCollection, AccountItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(AccountCollection, "/accounts/")
api.add_resource(AccountItem, "/accounts/<account>/")
