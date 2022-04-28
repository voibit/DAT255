#ifndef POST_H
#define POST_H

#include <QObject>
#include <QtQml/qqmlregistration.h>
#include <QString>
#include <QNetworkAccessManager>


class PostRequest : public QObject
{
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(QString response READ response WRITE setResponse NOTIFY responseChanged)

public:
    explicit PostRequest(QObject *parent = nullptr);

    const QString &response() const;
    void postMultipart(QUrl url, QString filename, QByteArray data, QString json=QString());
    Q_INVOKABLE void postMultipart(QUrl url, QUrl fileUrl, QString json=QString());
    Q_INVOKABLE void test();
public slots:
    void setResponse(const QString &newResponse);
    void slotFinished();


signals:

    void responseChanged(const QString &response);


private:
    QNetworkAccessManager *m_manager = nullptr;
    QString m_response;
};

#endif // BACKEND_H
