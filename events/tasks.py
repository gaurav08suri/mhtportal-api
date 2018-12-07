import logging
import requests
from celery import shared_task
from django.conf import settings
import json


logger = logging.getLogger(__name__)



@shared_task
def send_sms_async(type, params=None, headers={}):
    try:
        if type=='POST':
            data = {}
            headers = {}
            headers['authkey'] = settings.SMS_AUTH
            headers['Content-type'] = 'application/json'
            headers['Accept'] = 'text/plain'
            data['sender'] = settings.SENDER_ID
            data['country'] = settings.SMS_COUNTRY
            data['route'] = settings.SMS_ROUTE
            data['sms'] = [{'to': params['to'], 'message': params['message']}]
            #data['sms'] = [{'to': mobile, 'message': sms_string}]
            logger.info("In tasks, {}".format(settings.SMS_URL))
            #requests.post(url, headers=headers, data=params)
            requests.post(settings.SMS_URL, headers=headers, data=json.dumps(data))
            #requests.post(url, data=params)
        else:
            pass
            #requests.get(url)
    except requests.RequestException as e:
        logger.exception('While sending sms using requests')


