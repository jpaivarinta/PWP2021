import requests
import sys

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


### ACCOUNT related mehtods ###
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


#Run the application
main()

