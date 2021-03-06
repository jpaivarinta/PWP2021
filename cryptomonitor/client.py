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
                input("Too many attempts, press enter to continue")
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
    """
    Implements registering functionality
    """
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
            if password == password2 and password != "":
                break
            print("Passwords did not match or the given password was empty")
        resp = post_account(username, password)
    else:
        print("Bad response")


######################
### MENU FUNCTIONS ###
######################

def start_menu():
    """
    Implements start-menu for logging, registering and quitting in the client.
    """
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
            input("Invalid input, press enter to continue")
            continue


def main_menu():
    """
    Implements main-menu, where user can navigate to other menus
    """
    global logged_in
    # If user is logged out, program will return to start-menu
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
    """
    Implements menu for cryptocurrency relative actions.
    Prints the list of crypotcurrencies in the API and asks abbreviation for more specific information.
    """
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
            cresp = get_cryptocurrency(abbr)
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
    """
    Implements menu for portfolio relative actions.
    Prints the information about portfolio and asks user to edit portfolio or return.
    """
    while True:
        clear_terminal()
        print("\nPORTFOLIO INFORMATION:\n")
        pfolio_resp = get_portfolio(username)
        pc_resp = get_all_pcurrencies(username)
        # Checks if user has a portfolio
        if pfolio_resp.status_code == 200 and pc_resp.status_code == 200:
            pfolio_body = pfolio_resp.json()
            pc_body = pc_resp.json()
            if not pc_body["items"]:
                print("No cryptocurrencies in Portfolio\n")
            else:
                print("Total value: " + str(pfolio_body["value"]))
                print("Timestamp: " + str(pfolio_body["timestamp"]))
                print("Cryptocurrencies included:\n")
                for pcurrency in pc_body["items"]:
                    print("Cryptocurrency: " + pcurrency["currencyname"])
                    print("Amount: " + str(pcurrency["currencyamount"]) + "\n")

            print("(E) Edit portfolio")
            print("(R) Return")
            choice = input("Choose E or R: ").lower()
            if choice == 'r':
                return
            elif choice == 'e':
                pcurrency_menu()
            else:
                input("Invalid input. Press enter to continue: ")
        else:
            input("Portfolio not found, press enter to return")
            return


def pcurrency_menu():
    """
    Implements menu for actions relative to cryptocurrencies in user's portfolio.
    """
    while True:
        clear_terminal()
        print("\n*** EDIT PORTFOLIO ***\n")
        print("(A) Add cryptocurrency to portfolio")
        print("(E) Edit cryptocurrency amount")
        print("(D) Delete cryptocurrency from portfolio")
        print("(R) Return")
        choice = input("Choose A, E, D or R: ").lower()

        # Add cryptocurrency to portfolio
        if choice == 'a':
            abbr = input("Give abbreviation of cryptocurrency: ").lower()
            ccurrency = get_cryptocurrency(abbr)
            pcurrency = get_pcurrency(username, abbr)
            # Checks that currency not in portfolio
            if ccurrency.status_code == 200 and pcurrency.status_code == 404:
                amount = input("Give amount of cryptocurrency: ")
                # Checks if new amount is a number
                while (not check_float_input(amount)):
                    amount = input("Give amount of cryptocurrency: ")
                post_resp = post_pcurrency(username, abbr, amount)
                if post_resp.status_code == 201:
                    input("Cryptocurrency added to portfolio, press enter to continue")
                else:
                    input("Adding cryptocurrency failed, press enter to continue. ")
            else:
                input("Cryptocurrency doesn't exist or it is already in portfolio, press enter to continue.")

        # Edit cryptocurrency amount
        elif choice == 'e':
            abbr = input("Give abbreviation of cryptocurrency in the portfolio: ").upper()
            pcurrency = get_pcurrency(username, abbr)
            if pcurrency.status_code == 200:
                new_amount = input("Give new amount: ")
                # Checks if new amount is a number
                while (not check_float_input(new_amount)):
                    new_amount = input("Give new amount: ")
                put_resp = put_pcurrency(username, abbr, float(new_amount))
                if put_resp.status_code == 204:
                    input("Changes saved, press enter to continue")
                else:
                    input("Editing portfolio failed, press enter to continue. ")
            else:
                input("Cryptocurrency not found in the portfolio, press enter to continue.")

        # Delete cryptocurrency from portfolio
        elif choice == 'd':
            abbr = input("Give abbreviation of cryptocurrency in the portfolio: ").upper()
            resp = delete_pcurrency(username, abbr)
            if resp.status_code == 204:
                input("Cryptocurrency has been removed from portfolio")
            else:
                input("Cryptocurrency not found in the portfolio, press enter to continue.")
        elif choice == 'r':
            return
        else:
            input("Invalid input. Press enter to continue: ")


def account_menu():
    """
    Implements menu for choosing actions relative to user's account.
    """
    global username
    global logged_in
    while True:
        clear_terminal()
        acc_resp = get_account(username)
        # Checks if account is found
        if acc_resp.status_code == 200:
            print("\nACCOUNT INFORMATION:\n")
            acc_body = acc_resp.json()
            pfolio_url = acc_body["@controls"]["portfolio"]["href"]
            pfolio_resp = requests.get(API_URL + pfolio_url)
            pfolio_body = pfolio_resp.json()
            print("Name: " + str(acc_body["name"]))
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
                        # If account is deleted, user is logged out
                        logged_in = False
                        return
                    elif confirm == "n":
                        break
                    else:
                        print("Invalid input.")
            elif choice == "r":
                return
            else:
                input("Invalid input. Press enter to continue: ")


def edit_account():
    """
    Implements menu and actions for editing user's account.
    """
    global username
    while True:
        clear_terminal()
        print("\nEDIT ACCOUNT:\n")
        print("(N) Edit name")
        print("(P) Edit password")
        print("(R) Return")
        edit_choice = input("Choose N, P or R: ").lower()
        # Editing account's name
        if edit_choice == "n":
            new_name = input("Insert your new account name: ")
            pwd = input("Insert your password to continue: ")
            current_account = get_account(username)
            body = current_account.json()
            if (pwd == body["password"]):
                resp = put_account(username, new_name, pwd)
                if resp.status_code == 204:
                    username = new_name
                    input("Username has been changed successfully, press enter to continue")
                elif resp.status_code == 409:
                    input("Username already used, press enter to continue")
                else:
                    input("An error occurred while changing username, press enter to continue")
            else:
                input("Incorrect password, press enter to continue")
            continue
        # Editing account's password
        elif edit_choice == 'p':
            old_password = input("Insert your current password: ")
            current_account = get_account(username)
            body = current_account.json()
            if (old_password == body["password"]):
                new_password = input("Insert your new password: ")
                new_password2 = input("Insert your new password again: ")
                if (new_password == new_password2 and new_password != ""):
                    resp = put_account(username, username, new_password)
                    if resp.status_code == 204:
                        input("Password has been changed successfully, press enter to continue")
                    else:
                        input("An error occurred while changing password, press enter to continue")
                else:
                    input("Your given passwords didn't match or it was empty, press enter to continue")
                    continue
            else:
                input("Incorrect password, press enter to continue")
                continue

            continue
        elif edit_choice == "r":
            return
        else:
            input("Invalid input, press enter to continue. ")
            continue


########################
### ACCOUNT REQUESTS ###
########################

def get_all_accounts():
    """
    Get all accounts' informations.
    :return: API's response.
    """
    resp = requests.get(API_URL + "/api/accounts/")
    return resp


def post_account(name, password):
    """
    Post a new account.
    :param str name: name for the account
    :param str password: password for the account
    :return: API's response.
    """
    data = {}
    data["name"] = name
    data["password"] = password
    resp = requests.post(API_URL + "/api/accounts/", json=data)
    return resp


def get_account(username):
    """
    Get account's information.
    :param str username: name of the account
    :return: API's response.
    """
    account_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = requests.get(account_url)
    return resp


def put_account(username, new_username, new_passwd):
    """
    Edit account's information.
    :param str username: name of the account
    :param str new_username: new name for the account
    :param str new_passwd: new password for the account
    :return: API's response.
    """
    data = {}
    data["name"] = new_username
    data["password"] = new_passwd
    resp = requests.put(API_URL + "/api/accounts/" + username + "/", json=data)
    return resp


def delete_account(username):
    """
    Delete account.
    :param str username: name of the account
    :return: API's response.
    """
    delete_url = API_URL + "/api/accounts/" + str(username) + "/"
    resp = requests.delete(delete_url)
    return resp


##########################
### PORTFOLIO REQUESTS ###
##########################

def get_portfolio(username):
    """
    Get user's portfolio.
    :param str username: Name of the account
    :return: Request response object from the server.
    """
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/"
    resp = requests.get(get_url)
    return resp


def get_pcurrency(username, abbr):
    """
    Get a user's cryptocurrency in the portfolio.
    :param str username: Name of the account
    :param str abbr: Abbreviation of the cryptocurrency.
    :return: Request response object from the server.
    """
    pcurrency_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/" + str(abbr).upper() + "/"
    resp = requests.get(pcurrency_url)
    return resp


def get_all_pcurrencies(username):
    """
    Get a collection of user's cryptocurrencies in the portfolio.
    :param str username: Name of the account
    :return: Request response object from the server.
    """
    get_url = API_URL + "/api/accounts/" + str(username) + "/portfolio/pcurrencies/"
    resp = requests.get(get_url)
    return resp


def post_pcurrency(username, currency_abbreviation, currency_amount):
    """
    Add new cryptocurrency to user's portfolio.
    :param str username: Name of the account
    :param str currency_abbreviation: Abbreviation of cryptocurrency.
    :param str currency_amount: Amount of cryptocurrency
    :return: Request response object from the server.
    :note currency_abbreviation must be one of the existing currencies in the database.
    """
    currency_abbreviation = currency_abbreviation.upper()
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/".format(API_URL, username)
    pcurrency_body = {"currencyname": "{}".format(currency_abbreviation), "currencyamount": float(currency_amount)}
    resp = requests.post(pcurrency_url, json=pcurrency_body)
    return resp


def put_pcurrency(username, currency_abbreviation, currency_amount):
    """
    Edit cryptocurrency amount in user's portfolio.
    :param str username: Name of the account
    :param str currency_abbreviation: Abbreviation of cryptocurrency.
    :param str currency_amount: Amount of cryptocurrency
    :return: Request response object from the server.
    """
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/{}/".format(API_URL, username,
                                                                          currency_abbreviation.upper())
    pcurrency_json = get_pcurrency_json(currency_abbreviation, currency_amount)
    resp = requests.put(pcurrency_url, json=pcurrency_json)
    return resp


def delete_pcurrency(username, currency_abbreviation):
    """
    Remove cryptocurrency from user's portfolio.
    :param str username: Name of the account
    :param str currency_abbreviation: Abbreviation of cryptocurrency.
    :return: Request response object from the server.
    """
    pcurrency_url = "{}/api/accounts/{}/portfolio/pcurrencies/{}/".format(API_URL, username,
                                                                          currency_abbreviation.upper())
    resp = requests.delete(pcurrency_url)
    return resp


###############################
### CRYPTOCURRENCY REQUESTS ###
###############################

def get_all_cryptocurrencies():
    """ 
    Get all cryptocurrencies known by the API.
    :return: API's response.
    """
    resp = requests.get(API_URL + "/api/currencies/")
    return resp


def get_cryptocurrency(abbreviation):
    """ 
    Get a cryptocurrency known by the API.
    :param str abbreviation: Abbreviation of currency.
    :return: API's response.
    """
    currency_url = (API_URL + "/api/currencies/" + str(abbreviation).upper() + "/")
    resp = requests.get(currency_url)
    return resp


def clear_terminal():
    """ Clears the client's terminal. """
    os.system('cls' if os.name == 'nt' else 'clear')


# HELPER FUNCTIONS
def try_login(username, password):
    """
    Try login to account.
    :param str username: Username for the account
    :param str password: Password for the account
    :return: Return True or False whether login succeeds.
    """
    accounts_resp = get_all_accounts()
    body = accounts_resp.json()
    found = False
    for item in body["items"]:
        if item["name"] == username:
            # User found check if passwords match
            if item["password"] == password:
                return True
            else:
                return False

    print("Username not found, Try again\n")
    return False


def try_register(name, password1, password2):
    """
    Try register new account
    :param str name: Username for the account
    :param str password1: Password for the account
    :param str password2: Retyped password
    :return: Returns a string indicating the result.
    """
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
    """
    Creates a JSON
    :param str abbreviation: Abbreviation of the cryptocurrency
    :param str amount: amount of the cryptocurrency
    :return: json string
    """
    return {"currencyname": "{}".format(abbreviation.upper()), "currencyamount": float(amount)}


def get_account_json(name, password):
    """
    Creates a JSON
    :param str name: Username of the account
    :param str password: Password of the account
    :return: json string
    """
    return {"name": "{}".format(name), "password": "{}".format(password)}


def check_float_input(input):
    """
    Checks if input is number.
    :param str input:
    :return: Boolean
    """
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
