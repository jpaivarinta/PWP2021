import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Page {
    id: root
    property string username: ""

    ColumnLayout {
        id: columnLayout
        anchors.centerIn: parent

        Text {
            id: pagename_text
            text: qsTr("Account information")
            font.pixelSize: 16
        }

        Text {
            id: name_text
            text: qsTr("Name:")
            font.pixelSize: 12
        }

        Text {
            id: pfoliovalue_text
            text: qsTr("Portfolio value:")
            font.pixelSize: 12
        }

        Button {
            id: editaccount_button
            text: qsTr("Edit")
            onClicked: {
                pageStack.push("EditAccountPage.qml");
            }
        }

        Button {
            id: deleteaccount_button
            text: qsTr("Delete")
            onClicked: {
                foo.delete_account(foo.username);
                foo.username = ""
                pageStack.pop(null);
            }
        }
    }

    Component.onCompleted: {
        var account = foo.get_account(foo.username);
        var portfolio = foo.get_portfolio(foo.username);

        name_text.text = qsTr("Name: " + account.name);
        pfoliovalue_text.text = qsTr("Portfolio value: " + portfolio.value);
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
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
