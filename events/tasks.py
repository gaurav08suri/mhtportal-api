import logging
import requests
from celery import shared_task
from django.conf import settings
import json

logger = logging.getLogger(__name__)



@shared_task
def send_sms_async(type, params, headers={}):
    try:
        if type=='GET':
            requests.get(settings.SMS_URL_GET.format(settings.SMS_USER, settings.SMS_PASS, settings.SENDER_ID, params['to'], params['message']))
        elif type== 'POST':
            data = {}
            headers['authkey'] = settings.SMS_AUTH
            headers['Content-type'] = 'application/json'
            headers['Accept'] = 'text/plain'
            data['sender'] = settings.SMS_SENDER_ID
            data['country'] = settings.SMS_COUNTRY
            data['route'] = settings.SMS_ROUTE
            data['sms'] = [{'to': params['to'], 'message': params['message']}]
            requests.post(settings.SMS_URL_POST, headers=headers, data=json.dumps(data))

    except requests.RequestException as e:
        # should use logger here. I'll have to configure it.
        print('While sending sms using requests')


