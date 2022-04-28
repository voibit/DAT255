import QtQuick.Controls.Material
import QtQuick.Layouts
import QtMultimedia
import QtQml
import QtQuick

import PostRequest

ApplicationWindow {
    id:window
    Material.theme: Material.Dark
    Material.accent: Material.Cyan
    width: 640
    height: 480
    visible: true
    title: qsTr("Rest Post")
    property var inputs: []
    property bool recording : recorder.recorderState===MediaRecorder.RecordingState

    Timer {
        id: timer
        interval: 1000*interval.text
        running: false
        repeat: true
        onTriggered: {
            recorder.stop()
            delay.start()
        }
    }
    Timer {
        id: delay
        interval: 500
        repeat: false
        onTriggered: recorder.record()

    }

    MediaDevices { id: mediaDevices }

    MediaRecorder {
        id: recorder
        onRecorderStateChanged: {
            if(recorderState ===  MediaRecorder.StoppedState) {
                console.log("recoring stopped..")
                post.postMultipart("http://"+ip.text+":"+port.text, actualLocation)
            }
        }
        mediaFormat.fileFormat: MediaFormat.Wave

        onActualLocationChanged: {
            console.log(actualLocation)

        }
    }
    AudioInput { id: audioInput; muted: false }
    CaptureSession {
        id: captureSession
        recorder: recorder
        audioInput: audioInput
    }
    ColumnLayout{
        anchors.fill: parent
        Row{
            spacing: 8
            //anchors.fill: window
            Column {
                Label{text:"Input"}
                ComboBox {
                    id:selectInput
                    implicitWidth:250
                    model: mediaDevices.audioInputs
                    textRole: "description"
                    displayText: typeof currentValue === 'undefined' ? "Unavailable" : currentValue.description
                    onCurrentIndexChanged: audioInput.device = mediaDevices.audioInputs[currentIndex]
                }
            }
            Column {
                Label{text:"IP"}
                TextField {
                    id:ip
                    text: "127.0.0.1"
                    validator: RegularExpressionValidator {
                        regularExpression:  /^((?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){0,3}(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$/
                   }
                }
            }
            Column {
                Label{text:"Port"}
                TextField {
                    id:port
                    implicitWidth: 50
                    text: "8088"
                    validator: IntValidator {bottom:0;top:65535}

                }
            }
            Column {
                Label{text:"Interval[s]"}
                TextField {
                    id:interval
                    implicitWidth: 50
                    text: "100"
                    validator: IntValidator {bottom:1;top:1000}
                }
            }
            Column {
                Label{text:" "}
                Button {
                    text: recording? "stop" : "start"
                    onClicked: {
                        if(recording || timer.running) {
                            timer.stop()
                            recorder.stop()
                            delay.stop()
                            return
                        }
                        recorder.record()
                        timer.start()
                    }
                }
            }
            Rectangle {
                width:20
                height:20
                radius:10
                color: timer.running? "green": "gray"
            }

        }

        ListModel {
            id: listModel
        }

        Component {
                id: row
                Row {
                    spacing: 10
                    Text { text: key; color:"white"; font.pointSize: 22}
                    Text { text: value;color:"white"; font.pointSize: 22}
                }
            }

        ListView {
            id: list
            Layout.fillHeight: true
            Layout.fillWidth: true
            model:listModel
            delegate: row

            //text: post.response
        }
    }

    PostRequest {
        id: post
        onResponseChanged: (response)=> {
            listModel.clear()
            if(!response) return;
            let json = JSON.parse(response)
            if(json["error"]) {
                listModel.append({"key":"ERROR","value":json["error"]})
                return
            }
            for(const key in json) {
                console.log(key+json[key])
                listModel.append({"key":key,"value":json[key].toFixed(2)})
            }
        }

    }

}
