import requests

API_URL = "http://127.0.0.1:5000"

def main():
    print("*** CryptoMonitoring API Client ***")


def get_all_accounts():
    """Requests and print a list of all Accounts"""
    resp = request.get(API_URL + "/accounts/")
    body = resp.json()


main()

