import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from base.models import Participant
from base.tasks import send_sms_async

from django.db import connection


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Participant)
def generate_participant_code(sender, instance, **kwargs):
    pc = instance.first_name + "-" + instance.last_name + "-" + str(instance.date_of_birth.strftime("%d-%m-%Y"))
    pc = pc.lower()
    with connection.cursor() as cursor:
        check_if_exist_query = '''SELECT COUNT(1) FROM base_participant WHERE participant_code LIKE '{}%';'''.format(pc)
        cursor.execute(check_if_exist_query)

        existing_participant_code_count = cursor.fetchall()[0][0] or 0
        print("existing count==> ", existing_participant_code_count)
        if existing_participant_code_count == 0:
            instance.participant_code = pc
        else:
            pc = pc + '-{}'.format(existing_participant_code_count)
            instance.participant_code = pc


# @receiver(post_save, sender=Participant)
# def send_sms(sender, instance, created, **kwargs):
#     if created:
#         sms_string = 'Your Profile is now created. You can now login.'

#         # Because the sms vendor auto adds 91 to the number, we'll have to remove ours
#         # Note: This is a hack and only works for India numbers. Please don't use this in
#         # production.
#         mobile = str(instance.mobile)
#         if ('+' in mobile) or ('91' in mobile[0:3]):
#             mobile = mobile[3:]
#         url = settings.SMS_URL.format(settings.SMS_USER, settings.SMS_PASS, settings.SENDER_ID, mobile, sms_string)
#         try:
#             send_sms_async.delay(url)

#         except Exception as e:
#             logger.exception('while sending sms')


