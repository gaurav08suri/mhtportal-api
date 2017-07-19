from rest_framework import serializers
from events.models import (Event, EventParticipant)


class EventSerializer(serializers.ModelSerializer):
    """EventSerializer serializes Event model to json
    object and vice versa.
    """
    class Meta:
        model = Event
        exclude = ()



class EventParticipantSerializer(serializers.ModelSerializer):
    """EventParticipantSerializer serializes EventPariticpant model
    to json object and vice versa.
    """
    class Meta:
        model = EventParticipant
        exclude = ()
