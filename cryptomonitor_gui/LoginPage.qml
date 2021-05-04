
import QtQuick 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3


Page {
    id: root
    ColumnLayout {
        anchors.centerIn: parent

        MyTextInput{
            id:usernameInput
        }
        MyTextInput {
            id:passwordInput
        }

        Button {
            id: button_login
            text: "Login"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: {
                var name =  usernameInput.inputText.text;
                var psw = passwordInput.inputText.text;
                var logged = foo.login_clicked(name,psw)
                if (logged) {
                    console.log("logged in!!!")
                    foo.username=name
                    pageStack.push(mainmenuPage, {username: name})

                }
                else {
                    console.log("fuck you failed to log in")
                }
            }
        }
    }

    footer: ToolBar {
        id: bottomToolBar
        RowLayout {
            anchors.centerIn: parent

            ToolButton {
                text: qsTr("Back")
                onClicked: {
                    onClicked: pageStack.pop()
                }
            }
        }

    }
}
