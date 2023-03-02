import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 900
    height: 600
    title: "SAVIBot"

    Rectangle {
        anchors.fill: parent

        Image {
            anchors.fill: parent
            source: "static/Background.jpg"
            fillMode: Image.PreserveAspectCrop
        }

        Rectangle {
            anchors.fill : parent
            color: "transparent"

            Image {
                anchors.horizontalCenter : parent.horizontalCenter
                anchors.top : parent.top
                anchors.topMargin : 200
                source: "static/bubble.png"
            }
        }
    }

}