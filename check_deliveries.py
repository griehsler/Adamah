import json
import os
import logging
from datetime import datetime, timedelta

import api_client
import notification
import file_helper

configdir = 'config'
datadir = 'data'
logdir = 'log'

configfile = f'{configdir}/settings.json'
storagefile = f'{datadir}/storage.dat'
logfile = f'{logdir}/watcher.log'

file_helper.ensure_directories([configdir, datadir, logdir])

f = open(configfile, "r")
settings = json.load(f)
f.close()

adamahAccount = settings['adamahAccount']
adamahPassword = settings['adamahPassword']
mailSenderAccount = settings['mailSenderAccount']
mailSenderPassword = settings['mailSenderPassword']
recipients = settings.get('recipients', [])
disable_storage = settings.get('disableStorage', False)

file_helper.touch_file(logfile)
logging.basicConfig(filename=logfile, level=logging.INFO,
                    format='%(asctime)s %(message)s')


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


if disable_storage:
    last_handled = 0
else:
    last_handled = load_lasthandled()
handled = last_handled

token = api_client.login(adamahAccount, adamahPassword)

today = datetime.utcnow()
next_week = today + timedelta(days=7)

deliveries = api_client.getdeliveries(token, today, next_week)
new_deliveries = get_unhandled_populated(deliveries, last_handled)
if len(new_deliveries) == 0:
    logging.info('No new deliveries available')
for new_delivery in new_deliveries:
    #file_helper.dump_json(new_delivery, 'delivery.json')
    delivery_id = new_delivery['deliveryDate']
    logging.info(f'Found new delivery: {delivery_id}')
    logging.info(f'Sending notifications to {recipients}')
    notification.send_notifications(
        mailSenderAccount, mailSenderPassword, recipients, new_delivery)
    logging.info('Done sending notifications')
    handled = max([handled, delivery_id])

if (not disable_storage) and (handled != last_handled):
    store_lasthandled(handled)
    logging.info(f'Stored last handled delivery: {handled}')
