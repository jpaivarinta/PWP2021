
import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3


Page {
    id: root
    ColumnLayout {
        anchors.centerIn: parent

        Text {
            id: text_page_name
            text: qsTr("MAIN MENU")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        }


        ScrollView {
            id: scrollView
            width: 200
            height: 200
            Component {
                id: cryptocurrencyDelegate
                Item {
                    width:200;height:contentHeight
                    Column {
                        Text { text: "currency: " + name }
                        Text { text: "abbreviation: " + abbreviation}
                        Text { text: "value: " + value }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            var currency = foo.get_currency(abbreviation)
                            pageStack.push("CurrencyInfoPage.qml",{name: currency.name,
                                               abbreviation: currency.abbreviation, value: currency.value,
                                           timestamp: currency.timestamp, bclength: currency.blockchain_length,
                                           daily_growth: currency.daily_growth})
                        }
                    }
                }
            }

           ListView {
               anchors.fill: parent
               model: cryptocurrencyModel
               delegate: cryptocurrencyDelegate
           }
        }

        ListModel {
            id: cryptocurrencyModel
        }


    }
    Component.onCompleted: {
        // cryptocurrencyModel.append({name:"doge",value:200})
        var currency_list = foo.get_currencies()
        console.log(currency_list)
        for(var i in currency_list) {
            console.log(i)
            var currency = currency_list[i]
            cryptocurrencyModel.append({name:currency.name,abbreviation:currency.abbreviation,
                                           value:currency.value})
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
