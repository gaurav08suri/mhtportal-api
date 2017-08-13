from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from events.models import (Event,
                            EventParticipant)
from events.serializers import (EventSerializer,
                                EventParticipantSerializer)



class EventViewSet(ModelViewSet):
    """This endpoint Represents the Events in the system

    It can create/update/retrieve an Event
    It also presents lists of Events
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer



class EventParticipantViewSet(ModelViewSet):
    """This endpoint Represents the Event Participants

    It can create/update/retrieve an Event Participant
    It also presents lists of Event Participants
    """
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer



