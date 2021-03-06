
import QtQuick 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3


Page {
    id: root
    property string username: ""
    ColumnLayout {
        anchors.centerIn: parent

        Text {
            id: text_page_name
            text: qsTr("MAIN MENU")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        }
        Button {
            id:button_crypto
            text: qsTr("Cryprtocurrencies")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: pageStack.push("CryptoCurrenciesPage.qml")
        }

        Button {
            id:button_portfolio
            text: qsTr("Portfolio")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: {
                pageStack.push("PortfolioPage.qml")
            }
        }
        Button {
            id:button_account
            text: qsTr("Account")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: {
                pageStack.push("AccountPage.qml")
            }
        }

        Button {
            id: button_logout
            text: qsTr("Logout")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: {
                foo.username=""
                pageStack.pop()
            }
        }
    }
}
