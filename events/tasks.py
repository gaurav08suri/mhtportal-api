import logging
import requests
from celery import shared_task
from django.conf import settings
import json
from collections import defaultdict
from django.db import connection
from pusher import Pusher

logger = logging.getLogger(__name__)
pusher = Pusher(app_id= settings.PUSHER_APP_ID, key=settings.PUSHER_KEY, secret=settings.PUSHER_SECRET, cluster=settings.PUSHER_CLUSTER)


@shared_task()
def bulk_registeration(req_data):
    print('SOMETHING')
    event_code = 'EVENT_{}'.format(req_data['event_id'])
    if(settings.REDIS_CLIENT.exists(event_code) != 1):    
        with connection.cursor() as cursor:
            max_id_query = '''(select max(split_part(registration_no, '-', 4)::numeric) as max_id 
                                from events_eventparticipant where event_id = %s)'''
            cursor.execute(max_id_query,[req_data['event_id']])
            max_id_record = cursor.fetchall()
            settings.REDIS_CLIENT.set(event_code,max_id_record[0][0] or 1)    

    d = defaultdict(list)
    for r in req_data['participant_list']:
        d[r['id']] = [r['accommodation'], r['role']]

    participant_ids = [c['id'] for c in req_data['participant_list']]

    participant_query = '''with event_data as 
                                (select center_id, event_code from events_event where id = %s)
                            select bp.id as pid, bp.center_id as home_center_id, ed.center_id as event_center_id, 
                                        ed.event_code 
                            from base_participant bp, event_data ed
                            where bp.id = ANY(%s)'''

    with connection.cursor() as cursor:
        cursor.execute(participant_query, [req_data['event_id'], participant_ids])
        participant_records = cursor.fetchall()
        participant_input_query = '''INSERT INTO EVENTS_EVENTPARTICIPANT ( 
                                                            registration_no,
                                                            accommodation,
                                                            payment_status,
                                                            amount_paid,
                                                            cashier,
                                                            big_buddy,
                                                            goal_achievement,
                                                            role ,
                                                            event_id,
                                                            event_center_id,
                                                            home_center_id,
                                                            participant_id,
                                                            registration_status ,
                                                            created_on,
                                                            updated_on,
                                                            skill
                                                ) VALUES(%s,%s,false,0,'','','',%s,
                                                                %s,%s,%s,%s,2,current_timestamp,current_timestamp,'')'''
        for participant  in participant_records:      
            cursor.execute(participant_input_query,[
                participant[3] + '-M-{}'.format(settings.REDIS_CLIENT.incr(event_code)),
                d.get(participant[0])[0],
                d.get(participant[0])[1],
                req_data['event_id'],
                participant[2],
                participant[1],
                participant[0]
            ])
            send_registration_notification(participant[0])


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


def send_registration_notification(participant_id):
    print("in NOTIFIER")
    pusher.trigger(u'test-channel', u'my-event', {u'message': participant_id})

