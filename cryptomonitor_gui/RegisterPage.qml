import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Page {
    id:root
    ColumnLayout {
        anchors.centerIn: parent
        Text {
            id: status_text
        }
        MyTextInput{
            id:usernameInput
        }
        MyTextInput {
            id:passwordInput
        }
        MyTextInput {
            id:password2Input
        }

        Button {
            id: button_register
            text: "Register"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: {
                var name =  usernameInput.inputText.text;
                var psw = passwordInput.inputText.text;
                var psw2 = password2Input.inputText.text;
                var res = foo.register(name,psw, psw2)
                if (res==="success") {
                    pageStack.push(loginPage)
                }
                else {
                    status_text.text=res;
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
