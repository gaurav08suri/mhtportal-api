import logging
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from events.models import (Event, EventParticipant, EventCategory)
from base.models import (Participant, Address)
from base.serializers import (ParticipantSerializer,
                                AddressSerializer)



logger = logging.getLogger(__name__)



class EventSerializer(ModelSerializer):
    """EventSerializer serializes Event model to json
    object and vice versa.
    """
    venue = AddressSerializer()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('event_code',)



    def create(self, validated_data):
        address_data = validated_data.pop('venue')

        # only create if not already there
        try:
            address = Address.objects.get(**address_data)
        except Address.DoesNotExist:
            address = Address.objects.create(**address_data)
        except MultipleObjectsReturned:
            raise ValidationError

        event = Event.objects.create(venue=address, **validated_data)
        logger.info('Created Event {}'.format(event.name))

        return event



    def update(self, instance, validated_data):
        address_data = validated_data.pop('venue')

        # update participant
        for key, value in address_data.items():
            setattr(instance.venue, key, value)

        # update event participant data
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.venue.save()
        instance.save()
        logger.info('Updated Event {}'.format(instance.name))

        return instance



class EventCategorySerializer(ModelSerializer):
    """CenterSerializer serializes the Center model
    into json object and vice versa.
    """

    class Meta:
        model = EventCategory
        fields = '__all__'




class EventParticipantSerializer(ModelSerializer):
    """EventParticipantSerializer serializes EventPariticpant model
    to json object and vice versa.
    """
    #event = EventSerializer()
    participant = ParticipantSerializer()

    class Meta:
        model = EventParticipant
        fields = '__all__'
        read_only_fields = ('registration_no',)

    def create(self, validated_data):
        # event_data = validated_data.pop('event')
        print(validated_data)
        participant_data = validated_data.pop('participant')

        # only create if not already there
        try:
            participant = Participant.objects.get(**participant_data)
        except Participant.DoesNotExist:
            participant = Participant.objects.create(**participant_data)
        except MultipleObjectsReturned:
            raise ValidationError

        event_participant = EventParticipant.objects.create(participant=participant, **validated_data)
        logger.info('Created Event Participant. Registration no: {}'.format(event_participant.registration_no))

        return event_participant



    def update(self, instance, validated_data):
        participant_data = validated_data.pop('participant')

        # update participant
        for key, value in participant_data.items():
            setattr(instance.participant, key, value)

        # update event participant data
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.participant.save()
        instance.save()
        logger.info('Updated Event Participant. Registration no: {}'.format(instance.registration_no))

        return instance


