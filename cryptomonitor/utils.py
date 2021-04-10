import json
from flask import Response, request, url_for
from .models import UserAccount, Portfolio, CryptoCurrency

class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

class CryptoMonitorBuilder(MasonBuilder):

    @staticmethod
    def account_schema():
        schema = {
            "type": "object",
            "required": ["name", "password"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name of user",
            "type": "string"
        }
        props["password"] = {
            "description": "Password of account",
            "type": "string"
        }
        return schema

    @staticmethod
    def portfolio_schema():
        pass

    @staticmethod
    def pcurrency_schema(): #IS THIS ONE NEEDED?
        pass




    """ ACCOUNT controls """

    def add_control_all_accounts(self):
        """
        Adds control for all accounts in the response body.
        """
        self.add_control(
            "crymo:accounts-all",
            href=api.url_for("api.accounts"),
            method="GET",
            encoding="JSON"
        )
 
    def add_control_add_account(self):
        """
        Adds control for adding an account in the response body.
        """
        self.add_control(
            "crymo:add-account",
            href=api.url_for("api.accounts"),
            method="POST",
            encoding="JSON",
            title="Add new account",
            schema=self.account_schema()

        )

    def add_control_edit_account(self, account_id):
        """
        Adds control for editing an account in the response body.
        : param int account id: The ID of the editable account.
        """
        self.add_control(
            "edit",
            href=api.url_for("api.accounts", id=account_id),
            method="PUT",
            encoding="JSON",
            title="Edit account",
            schema=self.account_schema()
        )

    def add_control_delete_account(self, account_id):
        """
        Adds control for deleting an account in the response body.
        : param int account_id: The is of the deletable account.
        """
        self.add_control(
            "crymo:delete",
            href=api.url_for("api.accounts", id=account_id),
            method="DELETE",
            title="Delete this account"
        )


    """ PCURRENCY controls """

    def add_control_all_pcurrencies(self, account_id):
        """
        Add control for getting all pcurrencies.
        """
        self.add_control(
            "crymo:pcurrencies-all",
            href=api.url_for("api.pcurrencies", id=account_id),
            method="GET",
            encoding="JSON",
            title="Cryptocurrencies in account's portfolio"
        )

    def add_control_add_pcurrency(self, account_id, currency):
        """
        Add control for adding currencies into account's portfolio.
        """
        self.add_control(
            "crymo:add-pcurrency",
            href=api.url_for("api.pcurrencies", account=account_id, currencyname=currency),
            method="POST",
            encoding="JSON",
            title="Add currency to account's portfolio"
        )

    def add_control_delete_pcurrency(self, account_id, pcurrency_id):
        """
        Add control for deleting cryptocurrency from account's portfolio. 
        """
        self.add_control(
            "crymo:delete",
            href=api.url_for("api.pcurrency", account=account_id, pcurrencyId=pcurrency_id),
            method="DELETE",
            title="Delete cryptocurrency from the account's portfolio."
        )
    def add_control_edit_pcurrency(self, account_id, currency):
        """ 
        Add control for editing pcurrency.
        """
        self.add_control(
            "edit",
            href=api.url_for("api.pcurrency",account=account_id, currencyname=currency),
            method="PUT",
            encoding="JSON",
            title="Edit pcurrency in portfolio"
        )

    def add_control_get_currency_info(self, currencyname)
        """ 
        Add control for getting cryptocurrency info.
        """
        self.add_control(
            "crymo:currency-info",
            href=api.url_for("api.cryptocurrencies", currency=currencyname),
            method="GET",
            encoding="JSON",
            title="Informtion about cryptocurrency"
        )

    """ CRYPTOCURRENCY controls """

    def add_control_all_currencies(self):
        pass
    

def create_error_response(status_code, title, message=None):
    """
    Creates error response with status code, title and message.
    """
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)