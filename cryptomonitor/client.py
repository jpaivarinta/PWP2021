import requests
import os
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
            if name_input == "":
                return
            for item in body["items"]:
                if name_input == item["name"]:
                    found = True
                    username = name_input
                    break
            if found == True:
                break
            print("Username not found, try again or press enter to return\n")
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
        resp = post_account(username, password)
    else:
        print("Bad response")

######################
### MENU FUNCTIONS ###
######################

def start_menu():
    while True:
        clear_terminal()
        print("\n*** CryptoMonitoring API Client ***")
        print("\nSTART MENU\n")
        print("Choose the functionality you want to use:")
        print("(L) Login")
        print("(R) Register")
        print("(Q) Quit")
        choice = input("Type L, R or Q: ").lower()
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
            input("Invalid input, press anything to continue")
            continue

def main_menu():
    global logged_in
    while True:
        if logged_in == False:
            return
        clear_terminal()
        print("\n*** MAIN MENU ***")
        print("\nChoose the functionality you want to use:")
        print("(C) Cryptocurrencies")
        print("(P) Portfolio")
        print("(A) Account")
        print("(L) Log out")
        choice = input("Choose C, P, A or L: ").lower()
        clear_terminal()

        if choice == "c":
            print("Cryptocurrencies chosen")
            cryptocurrency_menu()
        elif choice == "p":
            print("Portfolio chosen")
            portfolio_menu()
        elif choice == "a":
            print("Account chosen")
            account_menu()
        elif choice == "l":
            print("Logging out")
            logged_in = False
            return
        else:
            print("invalid input, Try again\n")

def cryptocurrency_menu():
    clear_terminal()
    resp = get_all_cryptocurrencies()
    if resp.status_code == 200:
        body = resp.json()
        print("\nCRYPTOCURRENCIES:\n")
        for ccurrency in body["items"]:
            print(ccurrency["name"] + " | " + ccurrency["abbreviation"])
        while True:
            abbr = input("\nType abbreviation of cryptocurrency for more information, or 'r' to return: ").lower()
            if abbr == "r":
                clear_terminal()
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
        clear_terminal()
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
            print("(E) Edit portfolio")
            print("(R) Return")
            choice = input("Choose E or R: ").lower()
            if choice == 'r':
                return
            elif choice == 'e':
                pcurrency_menu()
            else:
                input("Invalid input. Press anything to continue: ")
        else:
            input("Portfolio not found, press anything to return")
            return
    
def pcurrency_menu():

    while True:
        clear_terminal()
        print("\n*** EDIT PORTFOLIO ***\n")
        print("(A) Add cryptocurrency to portfolio")
        print("(E) Edit cryptocurrency amount")
        print("(D) Delete cryptocurrency from portfolio")
        print("(R) Return")
        choice = input("Choose A, E, D or R: ").lower()

        #Add cryptocurrency to portfolio
        if choice == 'a':
            abbr = input("Give abbreviation of cryptocurrency: ").lower()
            ccurrency = get_cryptocurrency(abbr)
            pcurrency = get_pcurrency(username, abbr)
            if ccurrency.status_code == 200 and pcurrency.status_code == 404: #Checks that currency not in portfolio
                amount = input("Give amount of cryptocurrency: ")
                while(not check_float_input(amount)):
                    amount = input("Give amount of cryptocurrency: ")
                post_resp = post_pcurrency(username, abbr, amount)
                if post_resp.status_code == 201:
                    input("Cryptocurrency added to portfolio, press anything to continue")
                else:
                    input("Adding cryptocurrency failed, press anything to continue. ")
            else:
                input("Cryptocurrency doesn't exist or it is already in portfolio, press anything to continue.")

        #Edit cryptocurrency amount
        elif choice == 'e':
            abbr = input("Give abbreviation of cryptocurrency in the portfolio: ").upper()
            pcurrency = get_pcurrency(username, abbr)
            if pcurrency.status_code == 200:
                new_amount = input("Give new amount: ")
                while(not check_float_input(new_amount)):
                    new_amount = input("Give new amount: ")
                put_resp = put_pcurrency(username, abbr, float(new_amount))
                if put_resp.status_code == 204:
                    input("Changes saved, press anything to continue")
                else:
                    input("Editing portfolio failed, press anything to continue. ")
            else:
                input("Cryptocurrency not found in the portfolio, press anything to continue.")

        #Delete cryptocurrency from portfolio
        elif choice == 'd':
            abbr = input("Give abbreviation of cryptocurrency in the portfolio: ").upper()
            resp = delete_pcurrency(username, abbr)
            if resp.status_code == 204:
                input("Cryptocurrency has been removed from portfolio")
            else:
                input("Cryptocurrency not found in the portfolio, press anything to continue.")
        elif choice == 'r':
            return
        else:
            input("Invalid input. Press anything to continue: ")

def account_menu():
    global username
    global logged_in
    while True:
        clear_terminal()
        acc_resp = get_account(username)
        if acc_resp.status_code == 200:
            print("\nACCOUNT INFORMATION:\n")
            acc_body = acc_resp.json()
            pfolio_url = acc_body["@controls"]["portfolio"]["href"]
            pfolio_resp = requests.get(API_URL + pfolio_url)
            pfolio_body = pfolio_resp.json()
            print("Name: "+str(acc_body["name"]))
            print("Portfolio value: " + str(pfolio_body["value"]) + "\n")
            print("(E) Edit account")
            print("(D) Delete account")
            print("(R) Return")
            choice = input("Choose E, D or R: ")
            choice = choice.lower()
            if choice == "e":
                edit_account()                    
            elif choice == "d":
                while True:
                    confirm = input("Are you sure you want to delete account? Y or N: ")
                    confirm = confirm.lower()
                    if confirm == "y":
                        resp = delete_account(username)
                        username = ""
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

def edit_account():
    global username
    while True:
        clear_terminal()
        print("\nEDIT ACCOUNT:\n")
        print("(N) Edit name")
        print("(P) Edit password")
        print("(R) Return")
        edit_choice = input("Choose N, P or R: ").lower()
        if edit_choice == "n":
            new_name = input("Insert your new account name: ")
            pwd = input("Insert your password to continue: ")
            current_account = get_account(username)
            body = current_account.json()
            if(pwd == body["password"]):
                resp = put_account(username, new_name, pwd)
                if resp.status_code == 204:
                    username = new_name
                    input("Username has been changed successfully, press anything to continue")
                else:
                    input("An error occurred while changing username, press anything to continue")
            else:
                input("Incorrect password, press anything to continue")
            continue
        elif edit_choice == 'p':
            old_password = input("Insert your current password: ")
            current_account = get_account(username)
            body = current_account.json()
            if(old_password == body["password"]):
                new_password = input("Insert your new password: ")
                new_password2 = input("Insert your new password again: ")
                if(new_password == new_password2):
                    resp = put_account(username, username, new_password)
                    if resp.status_code == 204:
                        input("Password has been changed successfully, press anything to continue")
                    else:
                        input("An error occurred while changing password, press anything to continue")
                else:
                    input("Your given passwords didn't match, press anything to continue")
                    continue
            else:
                input("Incorrect password, press anything to continue")
                continue               
            
            continue
        elif edit_choice == "r":
            return
        else:
            input("Invalid input, press anything to continue. ")
            continue



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
    return resp

def get_account(username):
    """
    Prints given account's information.
    : param username: name of the printable account
    return: API's response.
    """
    account_url = API_URL + "/api/accounts/" + str(username) + "/"
    acc_resp = requests.get(account_url)
    return acc_resp

def put_account(username, new_username, new_passwd):
    #information = get_account_json(new_username, new_passwd)
    data = {}
    data["name"] = new_username
    data["password"] = new_passwd
    resp = requests.put(API_URL + "/api/accounts/" + username + "/", json=data)
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
    pcurrency_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/" + str(abbr).upper() + "/"
    resp = requests.get(pcurrency_url)
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
    pcurrency_body = {"currencyname": "{}".format(currency_abbreviation), "currencyamount": float(currency_amount)}
    # send post requests
    resp = requests.post(pcurrency_url, json=pcurrency_body)
    return resp

def put_pcurrency(username, currency_abbreviation, currency_amount):
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/{}/".format(API_URL,username,currency_abbreviation.upper())
    pcurrency_json = get_pcurrency_json(currency_abbreviation, currency_amount)
    resp = requests.put(pcurrency_url, json=pcurrency_json)
    return resp

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

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# HELPER FUNCTIONS
def try_login(username, password):
    accounts_resp = get_all_accounts()
    body = accounts_resp.json()
    found = False
    for item in body["items"]:
        if item["name"]==username:
            # User found check if passwords match
            if item["password"] == password:
                return True
            else:
                return False

    print("Username not found, Try again\n")
    return False

def try_register(name, password1, password2):
    accounts = get_all_accounts()
    if accounts.status_code == 200:
        body = accounts.json()
        taken = False
        username = name
        for item in body["items"]:
            if username == item["name"]:
                print("Username already taken")
                taken = True
                return "taken"

        if password1 != password2:
            print("Passwords did not match")
            return "mismatch"

        resp = post_account(username, password1)
        if resp.status_code == 201:
            return "success"
        else:
            return "Server fail"
    else:
        print("Bad response")
        return "Bad response from server"

def get_pcurrency_json(abbreviation, amount):
    return {"currencyname":"{}".format(abbreviation.upper()), "currencyamount":float(amount)}

def get_account_json(name, password):
    return {"name": "{}".format(name), "password": "{}".format(password)}

### TESTING FUNCTIONS ###

#get_all_accounts()
#post_account("test-account-7", "pswd7")
#get_account("test-account-1")
# get_all_cryptocurrencies()
#get_cryptocurrency("ETh")
# post_pcurrency("test-account-1", "eth", 2000.111)
# get_all_pcurrencies("test-account-1")
# put_pcurrency("test-account-1", "eth", 2.3)
# delete_pcurrency("test-account-1", "btc")
# get_all_pcurrencies("test-account-1")
#main_menu()
#get_portfolio("test-account-2")

def check_float_input(input):
    try:
        val = float(input)
        return True
    except ValueError:
        print("Wrong input type, value must be number")
        return False


logged_in = False

if __name__ == "__main__":
    while True:
        start_menu()
        main_menu()
#resp = get_pcurrency("test-account-2", "eth")
# print(resp)
#print(resp.json())



#resp = get_all_pcurrencies("test-account-2")
# print(resp.json())

