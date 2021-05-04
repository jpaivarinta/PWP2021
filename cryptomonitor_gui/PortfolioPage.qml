import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3


Page {
    id: root
    property string username: ""
    ColumnLayout {
        anchors.centerIn: parent

        Text {
            id: text_page_name
            text: qsTr("Portfolio information")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        }
        ColumnLayout {
            Text {
                id:totalvalue_text
                text:"total value"
            }
            Text {
                id: timestamp_text
                text: "timestamp"
            }
            Text {
                id: currencies_text
                text: "currencies:"
            }

            Rectangle {
                height: 200
                Layout.fillWidth: parent
//                color: "green"
            ScrollView {
                id: scrollView
                width: parent.width
                height: parent.height
                clip: true
                Component {
                    id: cryptocurrencyDelegate
                    Item {
                        width:200;height:contentHeight
                        Column {
                            Text { text: "currency name: " + abbreviation}
                            Text { text: "amount: " + amount }
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

            Button {
                id: editportfolio_button
                text: qsTr("Edit portfolio")
                onClicked: {
                    pageStack.push("PortfolioCurrencyPage.qml")
                }
            }
        }
    }
    Component.onCompleted: {
        // cryptocurrencyModel.append({name:"doge",value:200})
        var portfolio = foo.get_portfolio(foo.username)
        totalvalue_text.text = "total value: " + portfolio.value
        timestamp_text.text = "timestamp: " + portfolio.timestamp

        var currency_list = foo.get_pcurrencies(foo.username)
        console.log(currency_list)
        if(currency_list.length>0)
        {
            for(var i in currency_list) {
            console.log(i)
            var currency = currency_list[i]
            cryptocurrencyModel.append({abbreviation:currency.abbreviation, amount: currency.currencyAmount})
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
