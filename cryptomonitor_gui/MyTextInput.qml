import QtQuick 2.0
import QtQuick.Controls 2.5

Rectangle {
    height: 50
    width: root.width
    border.width: 1
    border.color: "red"
    color: "yellow"
    property TextInput inputText: input
    TextInput {
        id: input
        width:100
        height:50
        horizontalAlignment: Text.Center
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter

    }
}
