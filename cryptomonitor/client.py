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

def get_account_json(name, password):
    """
    Get valid account object.
    Args:
        name: Name of the account
        password: Password of the account

    Returns:
    Account object
    """
    return {"name": "{}".format(name), "password": "{}".format(password)}

def get_all_accounts():
    """Requests and prints a list of all Accounts"""
    resp = request.get(API_URL + "/api/accounts/")
    body = resp.json()
    print("ACCOUNTS:")
    for item in body["items"]:
        print("Id: "+str(item["id"]))
        print("Name: "+str(item["name"]))
        print("Portfolio-ID: "+str(item["portfolio_id"]))
    return resp

def post_account(username, passwd):
    information = get_account_json(username, passwd)
    resp = client.post(API_URL + "/api/accounts/", data=json.dumps(information))
    return resp

def get_account(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = client.get(get_url)
    acc_body = resp.json()

    pfolio = body["@controls"]["portfolio"]["href"]
    resp = client.get(get_url)
    pfolio_body = resp.json()

    print("ACCOUNT:")
    print("Name: " + str(acc_body["name"]))
    print("Portfolio value: " + str(pfolio_body["value"]))

    return acc_body, pfolio_body

def put_account(username, new_username, passwd):
    information = get_account_json(new_username, passwd)
    resp = client.put(API_URL + "/api/accounts/", data=json.dumps(information))
    return resp

def delete_account(username):
    delete_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = client.delete(delete_url)
    return resp

### Portfolio related methods ###
def get_portfolio(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/"
    resp = client.get(get_url)
    return resp
    

### PCurrency related methods ###
def get_all_pcurrencies(useraccount):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/"
    resp = client.get(get_url)
    body = json.loads(resp.data)
#    for item in body["items"]:
#        print(item[""])
    return resp

def post_pcurrency():
    pass



### CryptoCurrency related methods ###

def get_cryptocurrencies():
    return client.get(API_URL + "/api/currencies/")

def get_cryptocurrency(abbreviation):
    currency_url = (API_URL + "/api/currencies/" + str(abbrevation).lower() + "/")
    return client.get(currency_url) 


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

