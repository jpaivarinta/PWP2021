from flask_restful import Resource
from flask_restful import Api
from ..utils import CryptoMonitorBuilder
from ..utils import create_error_response

class PortfolioCurrency(Resource):
    def get(self,username, currencyname):
        pass
    def put(self, username, currencyname, currencyamount):
        pass
    def delete(self, username, currencyname):
        pass

class PortfolioCurrencies(Resource):
    def get(self, username):
        pass
    def post(self, username, currencyname, currencyamount):
        pass

