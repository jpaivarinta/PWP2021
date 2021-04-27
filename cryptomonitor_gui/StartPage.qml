import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Page {
    id: root
    ColumnLayout {
        id: column
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        Button {
            id: btn_login
            y: 0
            text: "login"
            onClicked: {
                pageStack.push(loginPage)
            }
        }
        Button {
            id: btn_register
            text: "register"
            onClicked: {
                pageStack.push(registerPage)
            }
        }
        Button {
            id: btn_quit
            text: "quit"
            onClicked: foo.quit("FUCK!!!")
        }
    }
}
