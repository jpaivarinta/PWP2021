# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtCore import QObject, Property, Slot, Signal
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from cryptomonitor.client import *


class CryptoCurrency(QObject):
    def __init__(self, name, abbreviation, value, parent=None):
        super().__init__(parent)
        self._name = name
        self._abbreviation = abbreviation
        self._value = value

    def get_name(self):
        return self._name

    def get_abbreviation(self):
        return self._abbreviation

    def get_value(self):
        return self._value

    name = Property(str, fget=get_name)
    abbreviation = Property(str, fget=get_abbreviation)
    value = Property(float, fget=get_value)


class PortfolioCurrency(QObject):
    def __init__(self, abbreviation, currencyAmount, parent=None):
        super().__init__(parent)
        self._abbreviation = abbreviation
        self._currencyAmount = currencyAmount

    def get_amount(self):
        return self._currencyAmount

    def get_abbreviation(self):
        return self._abbreviation

    currencyAmount = Property(float, fget=get_amount)
    abbreviation = Property(str, fget=get_abbreviation)


class Foo(QObject):
    cryptocurrenciesChanged = Signal()
    usernameChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cryptocurrencies = {}
        self._username = ""

    def get_cryptocurrencies(self):
        return self._cryptocurrencies

    cryptocurrencies = Property("QVariantList", fget=get_cryptocurrencies, notify=cryptocurrenciesChanged)

    def get_username(self):
        return self._username

    def set_username(self, user):
        if self._username != user:
            self._username = user
            self.usernameChanged.emit(self._username)

        username = Property(str, fget=get_username, fset=set_username, notify=usernameChanged)

    @Slot(str)
    def quit(self, msg):
        print(msg)
        qApp.quit()

    @Slot(str, str, result=bool)
    def login_clicked(self, username, password):
        print("Login: {} {}".format(username, password))
        return try_login(username, password)

    @Slot(str, str, str, result=str)
    def register(self, name, pswd1, pswd2):
        r = try_register(name, pswd1, pswd2)
        return r

    @Slot(str, result="QVariant")
    def get_account(self, name):
        resp = get_account(name)
        if resp.status_code == 200:
            return resp.json()

        r = {"name": ""}
        return r

    @Slot(str, result=bool)
    def delete_account(self, username):
        resp = delete_account(username)
        if resp.status_code == 204:
            return True
        return False

    @Slot(str, str, str, str, result=str)
    def edit_account(self, username, old_username, psw1, psw2):
        if psw1 == psw2:
            if username != old_username:
                resp = put_account(old_username, username, psw1)
                if resp.status_code == 204:
                    return "Success"
                elif resp.status_code == 409:
                    return "Name taken"
                else:
                    return "Pray god(s)!!!"
        else:
            return "Password mismatch"

    @Slot(result="QVariantList")
    def get_currencies(self):
        resp = get_all_cryptocurrencies()
        if resp.status_code == 200:
            body = resp.json()
            currencies = []
            for currency in body["items"]:
                print(currency["abbreviation"])
                currencies.append(
                    CryptoCurrency(name=currency["name"], abbreviation=currency["abbreviation"], value=200.2,
                                   parent=self))
            return currencies
        print(self._cryptocurrencies)

    @Slot(str, result="QVariant")
    def get_currency(self, abbr):
        resp = get_cryptocurrency(abbr)
        if resp.status_code == 200:
            body = resp.json();
            return body

    @Slot(str, result="QVariant")
    def get_portfolio(self, username):
        resp = get_portfolio(username)
        if resp.status_code == 200:
            return resp.json()

        r = {"value": "-1"}
        return r

    @Slot(str, result="QVariantList")
    def get_pcurrencies(self, username):
        resp = get_all_pcurrencies(username)
        pcurrencies = []
        if resp.status_code == 200:
            body = resp.json()
            for pc in body["items"]:
                pcurrencies.append(PortfolioCurrency(abbreviation=pc["currencyname"],
                                                     currencyAmount=pc["currencyamount"], parent=self))
            return pcurrencies
        else:
            print("fuck")
            return pcurrencies

    @Slot(str, str, str, result=bool)
    def add_pcurrency(self, username, currencyname, amount):
        amount = float(amount)
        resp = post_pcurrency(username, currencyname, amount)
        if resp.status_code == 201:
            return True
        else:
            return False

    @Slot(str, str, str, result=bool)
    def edit_pcurrency(self, username, abbr, amount):
        resp = put_pcurrency(username, abbr, float(amount))
        if resp.status_code == 204:
            return True
        else:
            return False

    @Slot(str, str, result=bool)
    def delete_pcurrency(self, username, currename):
        resp = delete_pcurrency(username, currename)

        if resp.status_code == 204:
            return True
        return False


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    foo = Foo()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("foo", foo)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
