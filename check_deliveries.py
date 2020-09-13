import json
import os
from datetime import datetime
from datetime import timedelta

import api_client
import notification

storagefile = 'storage.dat'

f = open('settings.json', "r")
settings = json.load(f)
f.close()

adamahAccount = settings['adamahAccount']
adamahPassword = settings['adamahPassword']
mailSenderAccount = settings['mailSenderAccount']
mailSenderPassword = settings['mailSenderPassword']
recipients = settings['recipients']


def store_lasthandled(sid):
    f = open(storagefile, "w")
    f.write(str(sid))
    f.close()


def load_lasthandled():
    if not os.path.isfile(storagefile):
        return 0
    f = open(storagefile, "r")
    if f.mode != "r":
        return 0
    sid = f.readline()
    f.close()
    try:
        return int(sid)
    except ValueError:
        return 0


def get_unhandled_populated(deliveries, last_handled_sid):
    populated_deliveries = list(filter(
        lambda delivery: 'contentDescPos' in delivery['deliveryPositions'][0]['productDetail'] and delivery['sid'] > last_handled_sid, deliveries))
    return populated_deliveries


last_handled = load_lasthandled()
handled = last_handled

token = api_client.login(adamahAccount, adamahPassword)

today = datetime.utcnow()
next_week = today + timedelta(days=7)

deliveries = api_client.getdeliveries(token, today, next_week)
new_deliveries = get_unhandled_populated(deliveries, last_handled)
for new_delivery in new_deliveries:
    notification.send_notifications(
        mailSenderAccount, mailSenderPassword, recipients, new_delivery)
    handled = max([handled, new_delivery['sid']])

if (handled != last_handled):
    store_lasthandled(handled)
