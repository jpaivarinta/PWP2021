
import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3


Page {
    id: root
    property string username: ""
    property string selected_currency: ""

    ColumnLayout {
        anchors.centerIn: parent

        Text {
            id: text_page_name
            text: qsTr("Edit currency amount")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        }


        ScrollView {
            id: scrollView
            anchors.centerIn: parent
            width: 600
            height: 200
            clip: true
            Component {
                id: cryptocurrencyDelegate
                Item {
                    width:contentWidth; height:contentHeight
                    Column {
                        Text { text: "currency name: " + abbreviation}
                        Text { text: "amount: " + amount }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            selected_currency = abbreviation
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

        Button {
            id: deletecurrency_button
            text: qsTr("Delete currency")
            onClicked:{
                if(selected_currency=="")
                    status_text.text = "Select currency."
                else
                {
                    var r = foo.delete_pcurrency(foo.username, selected_currency);
                    if(r)
                        status_text.text = "Success"
                    else
                        status_text.text = "Fail"
                }
            }
        }

        Text {
            id: status_text
        }


    }
    Component.onCompleted: {
        // cryptocurrencyModel.append({name:"doge",value:200})
        updateModel();
    }
    function updateModel()  {
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
