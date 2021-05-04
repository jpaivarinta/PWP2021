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
                pageStack.push("EditAccountPage.qml", {username: username});
            }
        }

        Button {
            id: deleteaccount_button
            text: qsTr("Delete")
            onClicked: {
                foo.delete_account(username);
                pageStack.pop();
            }
        }
    }

    Component.onCompleted: {
        var account = foo.get_account(username);
        var portfolio = foo.get_portfolio(username);

        name_text.text = qsTr("Name: " + account.name);
        pfoliovalue_text.text = qsTr("Portfolio value: " + portfolio.value);
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
