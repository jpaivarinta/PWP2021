import QtQuick 2.13
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Page {
    id: root
    property string  username: ""
    ColumnLayout {
        anchors.fill: parent
        Text{
            id: main_text
            text: "Edit portfolio"
            font.pointSize: 15
            fontSizeMode: Text.FixedSize
        }
        Button{
            id: addcurrency_button
            text: "Add cryptocurrency"
            onClicked: {
                pageStack.push("AddCurrencyPage.qml")
            }
        }

        Button {
            id: editcurrency_button
            text: "edit cryptocurrency amount"
            onClicked: {
                pageStack.push("EditCurrencyAmountPage.qml")
            }
        }

        Button {
            id: deletecurrency_button
            text: "Delete cryptocurrency"
            onClicked: {
                pageStack.push("DeleteCurrencyPage.qml")
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
