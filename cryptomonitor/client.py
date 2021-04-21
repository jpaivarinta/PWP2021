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



###############################
### ACCOUNT related methods ###
###############################

def get_all_accounts():
    """ Requests and prints a list of all Accounts"""
    resp = requests.get(API_URL + "/api/accounts/")
    if(resp.status_code == 200):
        body = resp.json()
        print("\nACCOUNTS:\n")
        for item in body["items"]:
            print("ID: "+str(item["id"]))
            print("Name: "+ item["name"])
            print("Password: " + item["password"])
            print("Portfolio-ID: "+str(item["portfolio_id"]) + "\n")
    else:
        print("Bad response")
    return resp

def post_account(name, password):
    """
    Posts a new account to database.
    : param name: name for the account
    : param password: password for the account
    return: API's response to post try.
    """
    print("ADD A NEW ACCOUNT")
    data = {}
    data["name"] = name
    data["password"] = password
    resp = requests.post(API_URL + "/api/accounts/", json=data)
    if(resp.status_code != 201):
        print("Bad response")
    else:
        print("Account added succesfully.")
    return resp

def get_account(username):
    """
    Prints given account's information.
    : param username: name of the printable account
    return: API's response.
    """
    account_url = API_URL + "/api/accounts/" + str(username) + "/"
    acc_resp = requests.get(account_url)
    if(acc_resp.status_code == 200):
        acc_body = acc_resp.json()
        pfolio_url = acc_body["@controls"]["portfolio"]["href"]
        pfolio_resp = requests.get(API_URL + pfolio_url)
        pfolio_body = pfolio_resp.json()
        print("ACCOUNT INFO:")
        print("ID: "+str(acc_body["id"]))
        print("Name: "+str(acc_body["name"]))
        #print("Password: "+str(acc_body["password"]))      #PASSWORD NOT SHOWN?
        print("Portfolio-ID: "+str(acc_body["portfolio_id"]))
        print("Portfolio value: " + str(pfolio_body["value"]) + "\n")
    return acc_resp

def put_account(username, new_username, passwd):
    information = get_account_json(new_username, passwd)
    resp = requests.put(API_URL + "/api/accounts/", data=json.dumps(information))
    return resp

def delete_account(username):
    delete_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = client.delete(delete_url)
    return resp



#################################
### Portfolio related methods ###
#################################
def get_portfolio(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/"
    resp = client.get(get_url)
    return resp
    

def get_all_pcurrencies(useraccount):

    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/"
    resp = client.get(get_url)
    body = json.loads(resp.data)
#    for item in body["items"]:
#        print(item[""])
    return resp

def post_pcurrency():
    pass

######################################
### CryptoCurrency related methods ###
######################################
def get_all_cryptocurrencies():
    """ 
    Print all cryptocurrencies known by the API.
    return: API's response.
    """
    resp = requests.get(API_URL + "/api/currencies/")
    if(resp.status_code == 200):
        body = resp.json()
        print("CRYPTOCURRENCIES:\n")
        for ccurrency in body["items"]:
            print("Currency: " + ccurrency["name"])
            print("Abbreviation: " + ccurrency["abbreviation"])
            print("Timestamp: " + ccurrency["timestamp"])
            print("Value: " + str(ccurrency["value"]))
            print("Daily growth: " + str(ccurrency["daily_growth"]) + "\n")
    else:
        print("Bad response")
    return resp

def get_cryptocurrency(abbreviation):
    """ 
    Print all cryptocurrencies known by the API.
    : param abbreviation: abbreviation of currency.
    return: API's response.
    """
    currency_url = (API_URL + "/api/currencies/" + str(abbreviation).lower() + "/")
    resp = requests.get(currency_url)
    if(resp.status_code == 200):
        body = resp.json()
        print("CRYPTOCURRENCY INFO:\n")
        print("Currency: " + body["name"])
        print("Abbreviation: " + body["abbreviation"])
        print("Timestamp: " + body["timestamp"])
        print("Value: " + str(body["value"]))
        print("Daily growth: " + str(body["daily_growth"]) + "\n")
    else:
        print("Bad response")
    return resp 




#OTHER METHODS
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


### TESTING FUNCTIONS ###

#get_all_accounts()
#post_account("test-account-7", "pswd7")
#get_account("test-account-1")
#get_all_cryptocurrencies()
#get_cryptocurrency("ETh")



