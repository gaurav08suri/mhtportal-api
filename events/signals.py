from django.utils import timezone
from django.db.models.signals import (pre_save,
                                        post_save)
from django.dispatch import receiver
from django.conf import settings
from base.models import Profile
from events.models import (Event,
                            EventParticipant)
from events.tasks import send_sms_async



@receiver(pre_save, sender=Event)
def generate_event_code(sender, instance, **kwargs):

    l = len(instance.name)
    s = ''
    y = instance.start_date.year
    if (l <= 6):
        s += instance.name.upper()
    else:
        words = instance.name.strip().split(' ')
        l = len(words)
        if (l == 1):
            s += words[0][:2].upper() + words[0][:-3:-1].upper()
        elif (l > 1 and l < 4):
            s += ''.join([w[i][:3].upper() for i, w in enumerate(words)])
        else:
            for i, w in enumerate(words):
                if (len(s) > 8):
                    break
                s += w[i][:i+1].upper()

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



@receiver(post_save, sender=EventParticipant)
def send_sms(sender, instance, created, **kwargs):
    if created:

        born = instance.participant.date_of_birth
        today = timezone.now().today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        # Get mobile number of coordinator of the center of the current pariticipant
        profile_filter = Profile.objects.filter(center=instance.home_center, gender=instance.participant.gender,
                                                min_age__lte=age, max_age__gte=age)
        if not profile_filter.exists():
            pm = ''
        else:
            pm = profile_filter.order_by('id').first().mobile

        sms_string = settings.SMS_TEMPLATE.format(instance.registration_no, int(instance.event.fees), pm)

        # Because the sms vendor auto adds 91 to the number, we'll have to remove ours
        # Note: This is a hack and only works for India numbers. Please don't use this in
        # production.
        mobile = str(instance.participant.mobile)
        if ('+' in mobile) or ('91' in mobile[0:3]):
            mobile = mobile[3:]
        url = settings.SMS_URL.format(settings.SMS_USER, settings.SMS_PASS, settings.SENDER_ID, mobile, sms_string)
        try:
            # pass
            send_sms_async.delay(url)

        except Exception as e:
            logger.exception('while sending sms')


