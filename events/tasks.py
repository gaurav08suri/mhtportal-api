import logging
import requests
from celery import shared_task



logger = logging.getLogger(__name__)



@shared_task
def send_sms_async(url, params=None):
    try:
        if params:
            requests.post(url, data=params)
        else:
            requests.get(url)
    except requests.RequestException as e:
        logger.exception('While sending sms using requests')


