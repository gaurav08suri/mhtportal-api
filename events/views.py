from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from url_filter.integrations.drf import DjangoFilterBackend
from events.models import (Event,
                            EventParticipant)
from events.serializers import (EventSerializer,
                                EventParticipantSerializer)
from events.permissions import IsAuthenticatedOrPostOnly



class EventViewSet(ModelViewSet):
    """This endpoint Represents the Events in the system

    It can create/update/retrieve an Event
    It also presents lists of Events
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'center', 'year', 'event_code', 'gender', 'min_age', 'max_age', 'active']



class EventParticipantViewSet(ModelViewSet):
    """This endpoint Represents the Event Participants

    It can create/update/retrieve an Event Participant
    It also presents lists of Event Participants
    """
    permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['id', 'event', 'participant', 'registration_no', 'home_center', 'event_center', 'accommodation',
     'payment_status', 'cashier', 'big_buddy', 'role', 'registration_status', 'created_on', 'updated_on']


