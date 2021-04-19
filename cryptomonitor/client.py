import requests
import sys
import json
from jsonschema import ValidationError

API_URL = "http://127.0.0.1:5000"

def main():
    main_menu()


def main_menu():
    print("*** CryptoMonitoring API Client ***")
    while True:
        print("Choose the functionality you want to use:\n")
        print("(A) Accounts")
        print("(C) CryptoCurrencies")
        print("(E) Exit application")
        choice = input("Type A, C or E: ")
        choice = choice.lower()

        if(choice == "a" or choice == "accounts"):
            print("Accounts chosen\n")
            return "ACCOUNTS"
        elif(choice == "c" or choice == "cryptocurrencies"):
            print("CryptoCurrencies chosen\n")
            return "CRYPTOCURRENCIES"
        elif(choice == "e" or choice == "exit"):
            print("Exit chosen, terminating app.")
            sys.exit()
        else:
            print("Invalid input, try again")
            continue


### ACCOUNT related methods ###
def get_all_accounts():
    """Requests and prints a list of all Accounts"""
    resp = request.get(API_URL + "/accounts/")
    body = resp.json()
    print("ACCOUNTS:")
    for item in body["items"]:
        print("Id: "+str(item["id"]))
        print("Name: "+str(item["name"]))
        print("Portfolio-ID: "+str(item["portfolio_id"]))

def post_account():
    pass
def get_account():
    pass
def put_account():
    pass
def delete_account():
    pass


### Portfolio related methods ###
def get_portfolio():
    pass

### PCurrency related methods ###
def get_all_pcurrencies():
    pass
def post_pcurrency():
    pass



### CryptoCurrency related methods ###

def get_cryptocurrencies():
    pass
def get_cryptocurrency():
    pass


def convert_value(value, schema_props):
    if schema_props["type"] == "number":
        try:
            value = int(value)
        except ValueError:
            value = float(value)
    if schema_props["type"] == "integer":
        value = int(value)
    if schema_props["type"] == "string":
        value = str(value)
    return value

def submit_data(s, ctrl, data):
    resp = s.request(
        ctrl["method"],
        "" + ctrl["href"],
        data=json.dumps(data),
        headers = {"Content-type": "application/json"}
    )
    return resp

#Run the application
main()

