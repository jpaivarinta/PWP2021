from flask_restful import Resource
from flask_restful import Api
from ..utils import CryptoMonitorBuilder
from ..utils import create_error_response

class CryptoCurrency(Resource):
    def get(self, name):
        pass

class CryptoCurrencyCollection(Resource):
    def get(self):
        pass