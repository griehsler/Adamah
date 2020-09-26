import smtplib
import ssl
from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime, timezone


def get_message(delivery):
    date = convert_date(delivery['deliveryDate'])
    detail = delivery['deliveryPositions'][0]['productDetail']
    name = detail['name']
    last_update = convert_date(delivery['latestOrderTime'])

    file_str = []
    if 'contentDescPos' in detail:
        for position in detail['contentDescPos']:
            productDetail = position['productDetail']
            file_str.append(
                f"{position['amount']} {productDetail['unit']} {productDetail['name']}")
    file_str.append('')
    file_str.append(f'Die Zusammenstellung kann noch bis {last_update:%d.%m. %H:%M} verändert werden.')

    message = MIMEText('\n'.join(file_str), 'plain', 'utf-8')
    message['Subject'] = Header(
        f'Die Zusammenstellung für "{name}" am {date:%d.%m.%Y} ist fertig!', 'utf-8')
    message['From'] = Header('Adamah Watcher')
    return message


def send_notifications(mailSenderAccount, mailSenderPassword, recipients, delivery):
    message = get_message(delivery)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as server:
        server.login(mailSenderAccount, mailSenderPassword)
        server.sendmail(mailSenderAccount, recipients, message.as_string())


def convert_date(unixtimestamp):
    return datetime.utcfromtimestamp(unixtimestamp/1000).replace(tzinfo=timezone.utc).astimezone(datetime.now().tzinfo)
