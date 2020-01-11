import re
import logging
import json
from django.utils import timezone
from django.db.models.signals import (pre_save,
                                      post_save)
from django.dispatch import receiver
from django.conf import settings
from base.models import (CenterScope,
                         Profile)
from events.models import (Event,
                           EventParticipant)
from events.tasks import send_sms_async
from django.db import connection


import json

logger = logging.getLogger(__name__)

center_event_poc = [
    {
        "center_id": 89,
        "mobile": 7069605637
    },
    {
        "center_id": 90,
        "mobile": "9601673613"
    },
    {
        "center_id": 4,
        "mobile": 9998992900
    },
    {
        "center_id": 5,
        "mobile": 9904312880
    },
    {
        "center_id": 44,
        "mobile": 9327072945
    },
    {
        "center_id": 63,
        "mobile": 9327072945
    },
    {
        "center_id": 39,
        "mobile": 9824090958
    },
    {
        "center_id": 64,
        "mobile": 9327081075
    },
    {
        "center_id": 70,
        "mobile": 9509300679
    },
    {
        "center_id": 68,
        "mobile": 7698025206
    },
    {
        "center_id": 6,
        "mobile": 9898026589
    },
    {
        "center_id": 7,
        "mobile": 9537977231
    },
    {
        "center_id": 71,
        "mobile": 8087137057
    },
    {
        "center_id": 72,
        "mobile": 9314209457
    },
    {
        "center_id": 8,
        "mobile": 9974299193
    },
    {
        "center_id": 9,
        "mobile": "9879822077"
    },
    {
        "center_id": 10,
        "mobile": "7359553949"
    },
    {
        "center_id": 73,
        "mobile": "9722324333"
    },
    {
        "center_id": 57,
        "mobile": "9428904747"
    },
    {
        "center_id": 75,
        "mobile": "9574046081"
    },
    {
        "center_id": 11,
        "mobile": "9825795751"
    },
    {
        "center_id": 65,
        "mobile": "6353468031"
    },
    {
        "center_id": 77,
        "mobile": "9205727818"
    },
    {
        "center_id": 12,
        "mobile": "9979109529"
    },
    {
        "center_id": 52,
        "mobile": "9904551649 / 7383818547"
    },
    {
        "center_id": 62,
        "mobile": "9926910037"
    },
    {
        "center_id": 78,
        "mobile": "7737806148"
    },
    {
        "center_id": 13,
        "mobile": "9428315109"
    },
    {
        "center_id": 53,
        "mobile": "7016861275"
    },
    {
        "center_id": 14,
        "mobile": "7984056061"
    },
    {
        "center_id": 66,
        "mobile": 8401389698
    },
    {
        "center_id": 15,
        "mobile": 9925678854
    },
    {
        "center_id": 16,
        "mobile": 8160590472
    },
    {
        "center_id": 17,
        "mobile": 9323263232
    },
    {
        "center_id": 18,
        "mobile": 9320819111
    },
    {
        "center_id": 19,
        "mobile": 9820597129
    },
    {
        "center_id": 20,
        "mobile": 7738044390
    },
    {
        "center_id": 21,
        "mobile": 9860708203
    },
    {
        "center_id": 22,
        "mobile": 9657003381
    },
    {
        "center_id": 79,
        "mobile": 9594982002
    },
    {
        "center_id": 80,
        "mobile": 9323263232
    },
    {
        "center_id": 23,
        "mobile": 8866100217
    },
    {
        "center_id": 24,
        "mobile": 9429290795
    },
    {
        "center_id": 81,
        "mobile": 9413172239
    },
    {
        "center_id": 82,
        "mobile": 8200041637
    },
    {
        "center_id": 25,
        "mobile": 9033494114
    },
    {
        "center_id": 27,
        "mobile": "8238990150"
    },
    {
        "center_id": 28,
        "mobile": "9726272267"
    },
    {
        "center_id": 26,
        "mobile": "9726272267"
    },
    {
        "center_id": 83,
        "mobile": "9824164941"
    },
    {
        "center_id": 50,
        "mobile": "9601301918"
    },
    {
        "center_id": 51,
        "mobile": 9924351117
    },
    {
        "center_id": 29,
        "mobile": 9898689697
    },
    {
        "center_id": 85,
        "mobile": 7359988465
    },
    {
        "center_id": 84,
        "mobile": 8758343332
    },
    {
        "center_id": 31,
        "mobile": 9904401775
    },
    {
        "center_id": 86,
        "mobile": 9898689697
    },
    {
        "center_id": 87,
        "mobile": 9537371313
    },
    {
        "center_id": 32,
        "mobile": 9998177813
    },
    {
        "center_id": 33,
        "mobile": 9825503819
    },
    {
        "center_id": 34,
        "mobile": 7405875164
    },
    {
        "center_id": 88,
        "mobile": "9427492610 / 7990098414"
    },
    {
        "center_id": 35,
        "mobile": 8200758658
    },
    {
        "center_id": 36,
        "mobile": "9924347260"
    }
]

@receiver(pre_save, sender=Event)
def generate_event_code(sender, instance, **kwargs):

    # no need to create if already there. I know there's a better way to
    # achieve this.
    if instance.event_code:
        return

    l = len(instance.name)
    s = ''
    y = instance.year
    if (l <= 6):
        s += instance.name.upper()
    else:
        only_alphanum = re.compile(r'[^a-zA-z0-9]')
        words = instance.name.strip().split(' ')
        l = len(words)

        # strip any non alphanumeric characters
        for i in range(l):
            words[i] = only_alphanum.sub('', words[i]).upper()

        if (l == 1):
            s += words[0][:2] + words[0][:-3:-1]
        elif (l > 1 and l < 4):
            s += ''.join([words[i][:3] for i in range(l)])
        else:
            for i in range(l):
                if (len(s) > 8):
                    break
                s += words[i][:i+1]

    fs = '{}-{}'.format(s, y)
    events = Event.objects.filter(event_code=fs)
    # event code not unique
    if events.exists():
        similar_events = len(events)
        instance.event_code = '{}-{}-{}'.format(s, similar_events+1, y)
    else:
        instance.event_code = fs


@receiver(pre_save, sender=EventParticipant)
def generate_registration_no(sender, instance, **kwargs):
    if settings.REDIS_CLIENT.exists(instance.event.event_code) != 1:
        with connection.cursor() as cursor:
            max_id_query = '''(select max(split_part(registration_no, '-', 4)::numeric) as max_id 
                                    from events_eventparticipant where event_id = %s)'''
            cursor.execute(max_id_query, [instance.event.id])
            max_id_record = cursor.fetchall()
            settings.REDIS_CLIENT.set(instance.event.event_code, max_id_record[0][0] or 1)

    if instance.registration_no:
        return

    ec = instance.event.event_code + '-M-'
    # if instance.participant.gender == 'male':
    #     ec += '-M-'
    # else:
    #     ec += '-F-'
    # last_registered = EventParticipant.objects.filter(event=instance.event,
    #                                                   participant__gender=instance.participant.gender).order_by('id').last()

    # if last_registered:
    #     total_registered = int(last_registered.registration_no.split('-')[-1])
    #     instance.registration_no = ec + '{}'.format(total_registered+1)
    # else:
    #     instance.registration_no = ec + '1'

    instance.registration_no = ec + '{}'.format(settings.REDIS_CLIENT.incr(instance.event.event_code))


@receiver(post_save, sender=EventParticipant)
def send_sms(sender, instance, created, **kwargs):

    if created:
        born = instance.participant.date_of_birth
        today = timezone.now().today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        is_lmht_or_bmht = (int(age) <= int(CenterScope.objects.filter(gender='').order_by('-max_age').first().max_age))
        profile_filter = None
        pm = ''
        gender = ''

        # Get mobile number of coordinator of the center of the current pariticipant
        # Profiles don't have gender for lmht and bmht. i.e. profiles are combined for boys and girls for lmht, bmht.
        if not is_lmht_or_bmht:
            gender = instance.participant.gender

        profile_filter = Profile.objects.filter(center=instance.home_center, gender=gender,
                                                min_age__lte=age, max_age__gte=age)

        # if age of participant is greater than any of the profiles, send the mobile no. of the profile of
        # the current event
        if not profile_filter.exists():
            profile_filter = Profile.objects.filter(center=instance.home_center, gender=gender,
                                                    min_age=instance.event.min_age, max_age=instance.event.max_age)

        if profile_filter.exists():
            pm = profile_filter.order_by('id').first().mobile

        if instance.event.id == 84:
            pm = "8200312214"

        if instance.event.id == 85:
            logger.info(instance.home_center)
            pms = [cep["mobile"] for cep in center_event_poc if cep["center_id"] == instance.home_center.id]
            if len(pms) > 0:
                pm = pms[0]
        
        if instance.event.is_global_poc == True:
            pm = instance.event.poc_number

        sms_string = settings.SMS_TEMPLATE.format(instance.registration_no, int(instance.event.fees), pm)

        # Because the sms vendor auto adds 91 to the number, we'll have to remove ours
        # Note: This is a hack and only works for India numbers. Please don't use this in
        # production.
        mobile = str(instance.participant.mobile)
        if ('+' in mobile) or ('91' in mobile[0:3]):
            mobile = mobile[3:]
        #url = settings.SMS_URL.format(settings.SMS_USER, settings.SMS_PASS, settings.SENDER_ID, mobile, sms_string)

        logger.info("Created SMS string {}".format(sms_string))
        try:
            # pass
            send_sms_async.delay('POST', params={'to': [mobile], 'message': sms_string})

        except Exception as e:
            logger.exception('while sending sms')
