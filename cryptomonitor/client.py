import requests
import sys
import json
from jsonschema import ValidationError
import msvcrt

API_URL = "http://127.0.0.1:5000"

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
            name_input = input("Username: ")
            for item in body["items"]:
                if name_input == item["name"]:
                    found = True
                    username = name_input
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
            taken = False
            username = input("Give your account an username: ")
            for item in body["items"]:
                if username == item["name"]:
                    print("Username already taken")
                    taken = True
            if taken:
                continue
            password = input("Give your account a password: ")
            password2 = input("Retype the password: ")
            if password == password2:
                break
            print("Passwords did not match")
        post_account(username, password)
    else:
        print("Bad response")

######################
### MENU FUNCTIONS ###
######################

def start_menu():
    print("\n*** CryptoMonitoring API Client ***")
    print("\nSTART MENU\n")
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

def main_menu():
    while True:
        print("\n*** MAIN MENU ***")
        print("\nChoose the functionality you want to use:")
        print("(C) Cryptocurrencies")
        print("(P) Portfolio")
        print("(A) Account")
        print("(L) Log out")
        choice = input("Choose C, P, A or L: ").lower()

        if choice == "c":
            print("Cryptocurrencies chosen")
            cryptocurrency_menu()
        elif choice == "p":
            print("Portfolio chosen")
            portfolio_menu()
        elif choice == "a":
            print("Account chosen")
            account_menu(username)
        elif choice == "l":
            print("Logging out")
            logged_in = False
            return
        else:
            print("invalid input, Try again\n")

def cryptocurrency_menu():
    resp = get_all_cryptocurrencies()
    if resp.status_code == 200:
        body = resp.json()
        print("\nCRYPTOCURRENCIES:\n")
        for ccurrency in body["items"]:
            print(ccurrency["name"] + " | " + ccurrency["abbreviation"])
        while True:
            abbr = input("\nType abbreviation of cryptocurrency for more information, or 'r' to return: ").lower()
            if abbr == "r":
                return
            cresp= get_cryptocurrency(abbr)
            if cresp.status_code == 200:
                cbody = cresp.json()
                print("\nCurrency: " + cbody["name"])
                print("Abbreviation: " + cbody["abbreviation"])
                print("Timestamp: " + cbody["timestamp"])
                print("Value: " + str(cbody["value"]))
                print("Daily growth: " + str(cbody["daily_growth"]))
    else:
        print("Bad response")
        return

def portfolio_menu():
    while True:
        print("\nPORTFOLIO INFORMATION:\n")
        pfolio_resp = get_portfolio(username)
        pc_resp = get_all_pcurrencies(username)
        if pfolio_resp.status_code == 200 and pc_resp.status_code == 200:
            pfolio_body = pfolio_resp.json()
            pc_body = pc_resp.json()
            print("Total value: " + str(pfolio_body["value"]))
            print("Timestamp: " + str(pfolio_body["timestamp"]))
            print("Cryptocurrencies included:\n")
            for pcurrency in pc_body["items"]:
                print("Cryptocurrency: "+ pcurrency["currencyname"])
                print("Amount: " + str(pcurrency["currencyamount"]) + "\n")
        while True:
            print("(E) Edit portfolio")
            print("(R) Return")
            choice = input("Choose E or R: ").lower()
            if choice == 'r':
                return
            elif choice == 'e':
                pcurrency_menu()
            else:
                input("Invalid input. Press anything to continue: ")
    
def pcurrency_menu():
    print("(A) Add cryptocurrency to portfolio")
    print("(E) Edit cryptocurrency amount")
    print("(D) Delete cryptocurrency from portfolio")
    print("(R) Return")
    while True:
        choice = input("Choose A, E, D or R: ").lower()
        if choice == 'a':
            abbr = input("Give abbreviation of cryptocurrency: ").lower()
            ccurrency = get_cryptocurrency(abbr)
            if ccurrency.status_code == 200: # Checks if cryptocurrency exists
                amount = input("Give amount of cryptocurrency: ") # Should this be float or string?
                post_pcurrency(username, abbr, amount)
            else:
                print("Cryptocurrency doesn't exist")
        elif choice == 'e':
            abbr = input("Give abbreviation of cryptocurrency in the portfolio: ").upper()
            pcurrency = get_pcurrency(username, abbr)
            if pcurrency.status_code == 200:
                new_amount = input("Give new amount: ")
                put_pcurrency(username, abbr, new_amount)
            else:
                print("Cryptocurrency not found in the portfolio")
        elif choice == 'd':
            abbr = input("Give abbreviation of cryptocurrency in the portfolio: ").upper()
            resp = delete_pcurrency(username, abbr)
            if resp.status_code == 204:
                print("Cryptocurrency has been removed from portfolio")
            else:
                print("Cryptocurrency not found in the portfolio")
        elif choice == 'r':
            return
        else:
            input("Invalid input. Press anything to continue: ")

def account_menu(username):
    acc_resp = get_account(username)
    if acc_resp.status_code == 200:
        print("\nACCOUNT INFORMATION:\n")
        acc_body = acc_resp.json()
        pfolio_url = acc_body["@controls"]["portfolio"]["href"]
        pfolio_resp = requests.get(API_URL + pfolio_url)
        pfolio_body = pfolio_resp.json()
        print("Name: "+str(acc_body["name"]))
        print("Portfolio value: " + str(pfolio_body["value"]) + "\n")
        while True:
            print("(E) Edit account")
            print("(D) Delete account")
            print("(R) Return")
            choice = input("Choose E, D or R: ")
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
            elif choice == "r":
                return
            else:
                input("Invalid input. Press anything to continue: ")



########################
### ACCOUNT REQUESTS ###
########################

def get_all_accounts():
    """ Requests a list of all Accounts"""
    resp = requests.get(API_URL + "/api/accounts/")
    if resp.status_code != 200:
        print("Bad response")
    return resp

def post_account(name, password):
    """
    Posts a new account to database.
    : param name: name for the account
    : param password: password for the account
    return: API's response to post try.
    """
    data = {}
    data["name"] = name
    data["password"] = password
    resp = requests.post(API_URL + "/api/accounts/", json=data)
    if resp.status_code != 201:
        print("Bad response")
    return resp

def get_account(username):
    """
    Prints given account's information.
    : param username: name of the printable account
    return: API's response.
    """
    account_url = API_URL + "/api/accounts/" + str(username) + "/"
    acc_resp = requests.get(account_url)
    if acc_resp.status_code != 200:
        print("Bad response")
    return acc_resp

def put_account(username, new_username, passwd):
    information = get_account_json(new_username, passwd)
    resp = requests.put(API_URL + "/api/accounts/", data=json.dumps(information))
    return resp

def delete_account(username):
    delete_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = requests.delete(delete_url)
    return resp



##########################
### PORTFOLIO REQUESTS ###
##########################

def get_portfolio(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/"
    resp = requests.get(get_url)
    if resp.status_code != 200:
        print("Bad response")
    return resp

def get_pcurrency(username, abbr):
    pcurrency_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/" + str(abbr) + "/"
    print(pcurrency_url)
    resp = requests.get(pcurrency_url)
    print(resp.status_code)
    return resp

def get_all_pcurrencies(username):
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/"
    resp = requests.get(get_url)
    if resp.status_code != 200:
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
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/{}/".format(API_URL,username,currency_abbreviation.upper())
    pcurrency_json = get_pcurrency_json(currency_abbreviation, currency_amount)
    resp = requests.put(pcurrency_url, json=pcurrency_json)
    if resp.status_code==204:
        print("Currency amount updated")
    else:
        print("Bad response")

def delete_pcurrency(username, currency_abbreviation):
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/{}/".format(API_URL, username, currency_abbreviation.upper())
    resp = requests.delete(pcurrency_url)
    #if resp.status_code == 204:
    #    print("Currency {} removed from portfolio".format(currency_abbreviation))
    #else:
    #    print("Bad response")
    return resp


###############################
### CRYPTOCURRENCY REQUESTS ###
###############################

def get_all_cryptocurrencies():
    """ 
    Print all cryptocurrencies known by the API.
    return: API's response.
    """
    resp = requests.get(API_URL + "/api/currencies/")
    if resp.status_code != 200:
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
    if resp.status_code != 200:
        print("Bad response")
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
# get_all_pcurrencies("test-account-1")
# put_pcurrency("test-account-1", "eth", 2.3)
# delete_pcurrency("test-account-1", "btc")
# get_all_pcurrencies("test-account-1")
#main_menu()
#get_portfolio("test-account-2")

#while True:
#   start_menu()
#    main_menu()
resp = get_pcurrency("test-account-2", "eth")
print(resp)
#print(resp.json())


"""
resp = get_all_pcurrencies("test-account-2")
print(resp.json())

"""