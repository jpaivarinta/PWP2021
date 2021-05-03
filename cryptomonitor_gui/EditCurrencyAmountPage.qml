
import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3


Page {
    id: root
    property string username: ""
    ColumnLayout {
        anchors.centerIn: parent

        Text {
            id: text_page_name
            text: qsTr("Edit currency amount")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        }


        ScrollView {
            id: scrollView
            width: 200
            height: 200
            clip: true
            Component {
                id: cryptocurrencyDelegate
                Item {
                    width:200;height:contentHeight
                    Column {
                        Text { text: "currency name: " + abbreviation}
                        Text { text: "amount: " + amount }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            var amount = currencyamount_input.inputText.text;
                            if(parseFloat(amount)<0)
                            {
                                status_text.text="Please input positive number";
                                return;
                            }

                            var r = foo.edit_pcurrency(username, abbreviation, amount )
                            if(r){
                                status_text.text = "Success"
                            } else {
                                status_text.text = "Fail"
                            }
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

        MyTextInput {
            id: currencyamount_input
        }
        Text {
            id: status_text
        }

        Button {
            id: button_logout
            text: qsTr("Logout")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            onClicked: pageStack.pop()
        }
    }
    Component.onCompleted: {
        // cryptocurrencyModel.append({name:"doge",value:200})
        var currency_list = foo.get_pcurrencies(username)
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
}
