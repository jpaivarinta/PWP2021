import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Window {
    id: window
    width: 1920
    height: 1080
    visible: true
    title: qsTr("Hello World")
    StackView {
        id: pageStack
        anchors.fill: parent
        initialItem: "StartPage.qml"
    }

    Component {
        id: loginPage
        LoginPage {

        }
    }

    Component {
        id: registerPage
        RegisterPage {

        }
    }
    Component {
        id: mainmenuPage
        MainMenuPage {

        }
    }

    Component {
        id:cryptocurrenciesPage
        CryptoCurrenciesPage {

        }
    }


}
