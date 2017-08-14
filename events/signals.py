import logging
from django.db.models.signals import pre_save
from django.dispatch import receiver
from events.models import (Event, 
                            EventParticipant)



logger = logging.getLogger(__name__)



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
    events = Event.objects.all().filter(event_code=fs)
    # event code not unique
    if events.exists():
        similar_events = len(events)
        instance.event_code = '{}-{}-{}'.format(s, similar_events+1, y)
    else:
        instance.event_code = fs

    logger.info('created event_code: {}'.format(instance.event_code))



@receiver(pre_save, sender=EventParticipant)
def generate_registration_no(sender, instance, **kwargs):
    ec = instance.event.event_code
    if instance.participant.gender == 'male':
        ec += '-M-'
    else:
        ec += '-F-'
    total_registered = len(EventParticipant.objects.all().filter(event=instance.event).order_by('id'))
    if total_registered:
        instance.registration_no = ec + str(total_registered+1)
    else:
        instance.registration_no = ec + '1'

    logger.info('created registration no: {}'.format(instance.registration_no))


