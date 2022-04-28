#include "post.h"
#include <QHttpMultiPart>
#include <QNetworkReply>
#include <QFile>

PostRequest::PostRequest(QObject *parent) : QObject(parent) {

    m_manager = new QNetworkAccessManager(this);
}

const QString &PostRequest::response() const {
    return m_response;
}

void PostRequest::postMultipart(QUrl url, QString filename, QByteArray data, QString json)
{
    setResponse("");
    QHttpMultiPart *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);

    if(!json.isEmpty()) {
        QHttpPart textPart;
        textPart.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("text/json"));
        textPart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant("form-data; name=\"json\""));
        textPart.setBody(json.toUtf8());
        multiPart->append(textPart);
    }

    QHttpPart dataPart;
    dataPart.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("application/octet-stream"));
    dataPart.setHeader(QNetworkRequest::ContentDispositionHeader,
                        QVariant(QString("form-data; name=\"file\"; filename=\"%1\"").arg(filename)));

    //QFile *file = new QFile("image.jpg");
    //file->open(QIODevice::ReadOnly);
    //imagePart.setBodyDevice(file)
    dataPart.setBody(data);
    multiPart->append(dataPart);

    QNetworkRequest request(url);
    QNetworkReply *reply = m_manager->post(request, multiPart);
    connect(reply, &QNetworkReply::finished, this, &PostRequest::slotFinished);
}

void PostRequest::postMultipart(QUrl url, QUrl fileUrl, QString json)
{
     QFile file(fileUrl.toLocalFile());

     file.open(QFile::ReadOnly);
     file.waitForReadyRead(1000);
     QByteArray test = file.readAll();
     postMultipart(url,fileUrl.fileName(),test, json);
}

void PostRequest::test()
{
    QUrl url("http://10.1.0.20:8088");
    QFile file("/Users/jk/Music/record_0006.m4a");
    file.open(QFile::ReadOnly);
    QByteArray test = file.readAll();
    postMultipart(url,"test.m4a",test);
}

void PostRequest::setResponse(const QString &newResponse)
{
    if (m_response == newResponse)
        return;
    m_response = newResponse;
    emit responseChanged(m_response);
}

void PostRequest::slotFinished()
{
    QNetworkReply *reply = dynamic_cast<QNetworkReply*>(sender());
    if(reply != nullptr) {
        setResponse(reply->readAll());
        reply->deleteLater();
    }

}
