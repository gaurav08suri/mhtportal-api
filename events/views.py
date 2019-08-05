from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from events.models import (Event,
                            EventParticipant, EventCategory)
from events.serializers import (EventSerializer,
                                EventParticipantSerializer,EventCategorySerializer)
from events.permissions import IsAuthenticatedOrPostOnly



class EventViewSet(ModelViewSet):
    """This endpoint Represents the Events in the system

    It can create/update/retrieve an Event
    It also presents lists of Events
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_fields = ['id', 'name', 'center', 'year', 'event_code', 'gender', 'min_age', 'max_age', 'active', 'category']



class EventCategoryViewSet(ModelViewSet):
    """This endpoint Represents the Centers

    It presents the list of Current Centers.
    """
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    filter_fields = ['id', 'category']




class EventParticipantViewSet(ModelViewSet):
    """This endpoint Represents the Event Participants

    It can create/update/retrieve an Event Participant
    It also presents lists of Event Participants
    """
    permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    filter_fields = ['id', 'event', 'participant', 'registration_no', 'home_center', 'event_center', 'accommodation',
     'payment_status', 'cashier', 'big_buddy', 'role', 'registration_status', 'created_on', 'updated_on']


