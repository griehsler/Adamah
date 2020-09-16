import json
import os
import logging
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import api_client
import notification

notification_active = True
persistence_active = True

storagefile = 'storage.dat'
logdir = 'logs'
logfile = '{}/watcher.log'.format(logdir)

f = open('settings.json', "r")
settings = json.load(f)
f.close()

adamahAccount = settings['adamahAccount']
adamahPassword = settings['adamahPassword']
mailSenderAccount = settings['mailSenderAccount']
mailSenderPassword = settings['mailSenderPassword']
recipients = settings['recipients']

if not Path(logdir).exists():
    Path(logdir).mkdir()
if not Path(logfile).exists():
    Path(logfile).touch()
logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s')

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


def get_unhandled_populated(deliveries, last_handled_id):
    populated_deliveries = list(filter(
        lambda delivery: 'contentDescPos' in delivery['deliveryPositions'][0]['productDetail'] and delivery['deliveryDate'] > last_handled_id, deliveries))
    return populated_deliveries


if persistence_active:
    last_handled = load_lasthandled()
else:
    last_handled = 0
handled = last_handled

token = api_client.login(adamahAccount, adamahPassword)

today = datetime.utcnow()
next_week = today + timedelta(days=7)

deliveries = api_client.getdeliveries(token, today, next_week)
new_deliveries = get_unhandled_populated(deliveries, last_handled)
if len(new_deliveries) == 0:
    logging.info('No new deliveries available')
for new_delivery in new_deliveries:
    delivery_id = new_delivery['deliveryDate']
    logging.info('Found new delivery: {}'.format(delivery_id))
    if (notification_active):
        logging.info('Sending notifications to {}'.format(recipients))
        notification.send_notifications(
            mailSenderAccount, mailSenderPassword, recipients, new_delivery)
        logging.info('Done sending notifications')
    else:
        logging.info('Would have sent notifications to {}'.format(recipients))
    handled = max([handled, delivery_id])

if persistence_active and (handled != last_handled):
    store_lasthandled(handled)
    logging.info('Stored last handled delivery: {}'.format(handled))
