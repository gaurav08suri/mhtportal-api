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

logger = logging.getLogger(__name__)

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

    # no need to create if already there. I know there's a better way to
    # achieve this.
    if instance.registration_no:
        return

    ec = instance.event.event_code
    if instance.participant.gender == 'male':
        ec += '-M-'
    else:
        ec += '-F-'
    last_registered = EventParticipant.objects.filter(event=instance.event,
                        participant__gender=instance.participant.gender).order_by('id').last()

    if last_registered:
        total_registered = int(last_registered.registration_no.split('-')[-1])
        instance.registration_no = ec + '{}'.format(total_registered+1)
    else:
        instance.registration_no = ec + '1'



#@receiver(post_save, sender=EventParticipant)
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


