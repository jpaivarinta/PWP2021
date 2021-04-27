# This Python file uses the following encoding: utf-8
import sys
import os

from PySide2.QtCore import QObject, QUrl, Slot
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from cryptomonitor.client import *



class Foo(QObject):
    @Slot(str)
    def quit(self, msg):
        print(msg)
        qApp.quit()

    @Slot(str, str, result=bool)
    def login_clicked(self, username, password):
        print("Login: {} {}".format(username,password))
        return try_login(username, password)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    foo = Foo()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("foo", foo)
    engine.load(os.path.join(os.path.dirname(__file__), "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
