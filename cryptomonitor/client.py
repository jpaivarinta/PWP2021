import requests
import sys
import json
from jsonschema import ValidationError

API_URL = "http://127.0.0.1:5000"

def main():
	start_menu()


def start_menu():
    print("*** CryptoMonitoring API Client ***")
    while True:
        print("Choose the functionality you want to use:\n")
        print("(L) Login")
        print("(R) Register")
        print("(Q) Quit")
        choice = input("Type L, R or Q: ")
        choice = choice.lower()

        if(choice == "l" or choice == "login"):
            print("Login chosen\n")
            return "LOGIN"
        elif(choice == "r" or choice == "register"):
            print("Register chosen\n")
            return "REGISTER"
        elif(choice == "q" or choice == "quit"):
            print("Quit chosen, terminating app.")
            sys.exit()
        else:
            print("Invalid input, try again")
            continue

def login():
    account = input("Accountname: ")
    password = input("Password: ")
    # resp = Re




### ACCOUNT related methods ###

def get_all_accounts():
    """Requests and prints a list of all Accounts"""
    resp = requests.get(API_URL + "/api/accounts/")
    body = resp.json()
    print("\nACCOUNTS:\n")
    for item in body["items"]:
        print("ID: "+str(item["id"]))
        print("Name: "+str(item["name"]))
        print("Password: "+str(item["password"]))
        print("Portfolio-ID: "+str(item["portfolio_id"]))
        print("")
    return resp

def post_account():
    print("ADD A NEW ACCOUNT")
    data = {}
    name = input("Type account name: ")
    pswd = input("Type password: ")
    data["name"] = name
    data["password"] = pswd
    print(data)
    resp = requests.post(API_URL + "/api/accounts/", json=data)
    print(resp)
    return resp

def get_account(username):
    account_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = requests.get(account_url)
    acc_body = resp.json()
    pfolio_url = acc_body["@controls"]["portfolio"]["href"]
    resp = requests.get(API_URL + pfolio_url)
    pfolio_body = resp.json()
    print("ACCOUNT:")
    print("Name: " + str(acc_body["name"]))
    print("Portfolio value: " + str(pfolio_body["value"]))

    return acc_body, pfolio_body

def put_account(username, new_username, passwd):
    information = get_account_json(new_username, passwd)
    resp = requests.put(API_URL + "/api/accounts/", data=json.dumps(information))
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
#main()
#get_all_accounts()
#post_account()
#login()
get_account("test-account-1")



