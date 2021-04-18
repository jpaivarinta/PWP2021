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

def get_all_accounts():
    """Requests and prints a list of all Accounts"""
    resp = request.get(API_URL + "/accounts/")
    body = resp.json()



#Run the application
main()

