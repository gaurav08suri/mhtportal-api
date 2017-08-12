import requests
from celery import shared_task



@shared_task
def send_sms_async(url, params=None):
    print('--------------')
    print('sending sms')
    try:
        if params:
            requests.post(url, data=params)
        else:
            print('calling get')
            print(url)
            requests.get(url)
    except requests.RequestException as e:
        print(e)


