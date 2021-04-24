import requests
import sys
import json
from jsonschema import ValidationError
import msvcrt

API_URL = "http://127.0.0.1:5000"


def start_menu():
    print("*** CryptoMonitoring API Client ***")
    print("START MENU\n")
    while True:
        print("Choose the functionality you want to use:")
        print("(L) Login")
        print("(R) Register")
        print("(Q) Quit")
        choice = input("Type L, R or Q: ")
        choice = choice.lower()

        if choice == "l" or choice == "login":
            print("Login chosen\n")
            login()
            if logged_in == True:
                break
            else:
                continue
        elif choice == "r" or choice == "register":
            print("Register chosen\n")
            register()
        elif choice == "q" or choice == "quit":
            print("Quit chosen, terminating app.")
            sys.exit()
        else:
            print("Invalid input, try again")
            continue

def login():
    """
    Implements Login-functionality
    """
    global logged_in, username
    username = ""
    logged_in = False
    accounts = get_all_accounts()
    if accounts.status_code == 200:
        body = accounts.json()
        attempts = 0
        while True:
            found = False
            username = input("Username: ")
            for item in body["items"]:
                if username == item["name"]:
                    found = True
                    break
            if found == True:
                break
            print("Username not found, Try again\n")
        while True:
            if attempts == 4:
                print("Too many attempts, going back to Start Menu")
                return
            password = input("Password: ")
            if password == item["password"]:
                break
            print("Invalid password")
            attempts += 1
        print("Login successful.\n")
        logged_in = True
        return
    else:
        print("Bad response")
        return

def register():
    accounts = get_all_accounts()
    if accounts.status_code == 200:
        body = accounts.json()
        while True:
            username = input("Give your account an username: ")
            for item in body["items"]:
                if username == item:
                    print("Username already taken")
                    continue
            break
        while True:
            password = input("Give your account a password: ")
            password2 = input("Retype the password: ")
            if password == password2:
                break
            print("Passwords did not match")
        post_account(username, password)
        start_menu()
    else:
        print("Bad response")

def main_menu():
    print("*** MAIN MENU ***\n")
    while True:
        print("Choose the functionality you want to use:")
        print("(C) Cryptocurrencies")
        print("(P) Portfolio")
        print("(A) Account")
        print("(L) Log out")
        choice = input("Choose C, P, A or L: ").lower()

        if choice == "c":
            print("Cryptocurrencies chosen")
            get_all_cryptocurrencies()
        elif choice == "p":
            print("Portfolio chosen")
            portfolio_menu()
        elif choice == "a":
            print("Account chosen")
            account_menu(username)
        elif choice == "l":
            print("Logging out")
            logged_in = False
            start_menu()
        else:
            print("invalid input, Try again\n")

def cryptocurrency_menu():
    cryptocurrencies = get_all_cryptocurrencies()
    if cryptocurrencies.status_code == 200:
        body = cryptocurrencies.json()
        print("CRYPTOCURRENCIES:\n")
        for ccurrency in body["items"]:
            print("Currency: " + ccurrency["name"] + "|" + "Abbreviation: " + ccurrency["abbreviation"])
    else:
        print("Bad response")
        return

    while True:
        abbr = input("Type abbreviation of cryptocurrency for more information, or 'exit' to return: ").lower()
        if abbr == "exit":
            return
        cryptocurrency = get_cryptocurrency(abbr)
        if cryptocurrency.status_code == 200:
            cbody = cryptocurrency.json()
            print("Currency: " + cryptocurrency["name"])
            print("Abbreviation: " + cryptocurrency["abbreviation"])
            print("Timestamp: " + cryptocurrency["timestamp"])
            print("Value: " + str(cryptocurrency["value"]))
            print("Daily growth: " + str(cryptocurrency["daily_growth"]))


def portfolio_menu():
    print("\nPORTFOLIO INFORMATION:\n")
    get_portfolio(username)


def account_menu(username):
    account = get_account(username)
    if account.status_code == 200:
        body = account.json()
        while True:
            print("(E) Edit account")
            print("(D) Delete account")
            print("(M) Main menu")
            choice = input("Choose E, D or M: ")
            choice = choice.lower()
            if choice == "e":
                pass
            elif choice == "d":
                while True:
                    confirm = input("Are you sure you want to delete account? Y or N: ")
                    confirm = confirm.lower()
                    if confirm == "y":
                        resp = delete_account(username)
                        logged_in = False
                        return 
                    elif confirm == "n":
                        break
                    else:
                        print("Invalid input.")
            elif choice == "m":
                main_menu()
            else:
                input("Invalid input. Press anything to continue: ")

###############################
### ACCOUNT related methods ###
###############################

def get_all_accounts():
    """ Requests and prints a list of all Accounts"""
    resp = requests.get(API_URL + "/api/accounts/")
    if resp.status_code == 200:
        body = resp.json()
        """
        print("\nACCOUNTS:\n")
        for item in body["items"]:
            print("ID: " + str(item["id"]))
            print("Name: " + item["name"])
            print("Password: " + item["password"])
            print("Portfolio-ID: " + str(item["portfolio_id"]) + "\n")
        """
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
    if resp.status_code != 201:
        print("Bad response")
    else:
        print("Account added successfully.")
    return resp

def get_account(username):
    """
    Prints given account's information.
    : param username: name of the printable account
    return: API's response.
    """
    account_url = API_URL + "/api/accounts/" + str(username) + "/"
    acc_resp = requests.get(account_url)
    if acc_resp.status_code == 200:
        acc_body = acc_resp.json()
        pfolio_url = acc_body["@controls"]["portfolio"]["href"]
        pfolio_resp = requests.get(API_URL + pfolio_url)
        pfolio_body = pfolio_resp.json()
        print("ACCOUNT INFO:")
        print("Name: "+str(acc_body["name"]))
        print("Portfolio-ID: "+str(acc_body["portfolio_id"]))
        print("Portfolio value: " + str(pfolio_body["value"]) + "\n")
    return acc_resp

def put_account(username, new_username, passwd):
    information = get_account_json(new_username, passwd)
    resp = requests.put(API_URL + "/api/accounts/", data=json.dumps(information))
    return resp

def delete_account(username):
    delete_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = requests.delete(delete_url)
    return resp



#################################
### Portfolio related methods ###
#################################
def get_portfolio(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/"
    resp = requests.get(get_url)
    if resp.status_code == 200:
        body = resp.json()
        print("Total value: " + str(body["value"]))
        print("Timestamp: " + str(body["timestamp"]))
        print("Cryptocurrencies included: \n")
        get_all_pcurrencies(username)
    else:
        print("Bad response")
    return resp
    

def get_all_pcurrencies(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/"
    resp = requests.get(get_url)
    if resp.status_code == 200:
        body = resp.json()
        for item in body["items"]:
            print("Cryptocurrency: "+ item["currencyname"])
            print("Amount: " + str(item["currencyamount"]) + "\n")
    else:
        print("Bad response")
    return resp

def post_pcurrency(username, currency_abbreviation, currency_amount):
    currency_abbreviation = currency_abbreviation.upper()
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/".format(API_URL, username)
    pcurrency_body = {"currencyname": "{}".format(currency_abbreviation), "currencyamount": "{}".format(currency_amount)}
    # send post requests
    resp = requests.post(pcurrency_url, json=pcurrency_body)
    if resp.status_code == 201:
        print("Currency added to portfolio")
    else:
        print("Bad response")

def put_pcurrency(username, currency_abbreviation, currency_amount):
    """
    TODO: @Sami fix this!!!
    Returns:
        object:
    """
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/{}/".format(API_URL,username,currency_abbreviation.upper())
    pcurrency_json = get_pcurrency_json(currency_abbreviation, currency_amount)
    resp = requests.put(pcurrency_url, json=pcurrency_json)
    if resp.status_code==204:
        print("Currency amount updated")
    else:
        print("Bad response")


######################################
### CryptoCurrency related methods ###
######################################
def get_all_cryptocurrencies():
    """ 
    Print all cryptocurrencies known by the API.
    return: API's response.
    """
    resp = requests.get(API_URL + "/api/currencies/")
    if resp.status_code == 200:
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
    currency_url = (API_URL + "/api/currencies/" + str(abbreviation).upper() + "/")
    resp = requests.get(currency_url)
    if resp.status_code == 200:
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

# HELPER FUNCTIONS
def get_pcurrency_json(abbreviation, amount):
    return {"currencyname":"{}".format(abbreviation.upper()), "currencyamount":"{}".format(amount)}

### TESTING FUNCTIONS ###

#get_all_accounts()
#post_account("test-account-7", "pswd7")
#get_account("test-account-1")
#get_all_cryptocurrencies()
#get_cryptocurrency("ETh")
# post_pcurrency("test-account-1", "eth", 2000.111)
#get_all_pcurrencies("test-account-1")
#put_pcurrency("test-account-1", "eth", 2.3)
#get_all_pcurrencies("test-account-1")
#main_menu()
#get_portfolio("test-account-2")

while True:
    start_menu()
    main_menu()