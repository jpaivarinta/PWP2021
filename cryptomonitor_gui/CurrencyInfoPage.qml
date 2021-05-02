
import QtQuick 2.5
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Page {
    property alias name: currencyName.text
    property alias abbreviation: currencyAbbreviation.text
    property alias value: currencyValue.text
    property alias timestamp: currencyTimestamp.text
    property alias bclength: currencybc_length.text
    property alias daily_growth: currencydaily_growth.text
    id: root
    ColumnLayout{
        anchors.centerIn: parent
        Text {
            id: currencyName
        }
        Text {
            id: currencyAbbreviation
        }
        Text {
            id: currencyValue
        }
        Text {
            id: currencyTimestamp
        }
        Text {
            id: currencybc_length
        }
        Text {
            id: currencydaily_growth
        }
    }
}
