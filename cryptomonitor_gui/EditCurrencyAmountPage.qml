
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
            font.pointSize: 15
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
                            var amount = currencyamount_input.inputText.text;
                            if(parseFloat(amount)<0)
                            {
                                status_text.text="Please input positive number";
                                return;
                            }

                            var r = foo.edit_pcurrency(foo.username, abbreviation, amount )
                            if(r){
                                status_text.text = "Success"
                                updateModel();
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

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
