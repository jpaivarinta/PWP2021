import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Page {
    id: root
    property string username: ""

    property alias newName_input: username_input.inputText
    property alias p1_input: pass1_input.inputText
    property alias p2_input: pass2_input.inputText

    ColumnLayout {
        id: columnLayout
        anchors.fill: parent

        MyTextInput {
            id: username_input
            inputText.text: "new username"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyTextInput {
            id: pass1_input
            inputText.text: "new password"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        MyTextInput {
            id: pass2_input
            inputText.text: "retype new password"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        Text {
            id: status_text
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        Button {
            id: cp_button
            text: qsTr("Change information")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: {
                var newName = newName_input.text
                var pass1 = p1_input.text
                var pass2 = p2_input.text

                var r = foo.edit_account(newName, username, pass1,pass2)
                if(r==="Success") {
                    foo.username = newName
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
/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.75;height:480;width:640}D{i:1}
}
##^##*/
