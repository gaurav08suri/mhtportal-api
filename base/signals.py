from django.db.models.signals import post_save
from django.dispatch import receiver
from mhtportal.settings import (SMS_URL,
                                SMS_USER,
                                SMS_PASS,
                                SENDER_ID) 
from base.models import Participant
from base.tasks import send_sms_async



@receiver(post_save, sender=Participant)
def send_sms(sender, instance, created, **kwargs):
    if created:
        sms_string = 'Your Registration is now Complete'
        # Because the sms vendor auto adds 91 to the number, we'll have to remove ours
        url = SMS_URL.format(SMS_USER, SMS_PASS, SENDER_ID, str(instance.mobile)[3:], sms_string)
        try:
            send_sms_async.delay(url)

        except Exception as e:
            print(e)


