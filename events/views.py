from django.db import connection

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Participant
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
    """This endpoint Represents the Event Category

    It presents the list of all the event catgories.
    """
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    filter_fields = ['id', 'category']




class EventParticipantViewSet(ModelViewSet):
    """This endpoint Represents the Event Participants

    It can create/update/retrieve an Event Participant
    It also presents lists of Event Participants
    """
    
    # permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = EventParticipant.objects.all()
    queryset = queryset.prefetch_related('participant')
    serializer_class = EventParticipantSerializer
    filter_fields = ['id', 'event', 'participant', 'registration_no', 'home_center', 'event_center', 'accommodation',
     'payment_status', 'cashier', 'big_buddy', 'role', 'registration_status', 'created_on', 'updated_on']

@api_view(['POST'])
def bulk_register(request):
    req_data = request.data
    participant_ids = [c['id'] for c in req_data['participant_list']]
    participant_query = '''with event_data as 
                                (select center_id, event_code from events_event where id = %s),
                           epd as 
                           (select max(split_part(registration_no, '-', 4)::numeric) as max_id 
                                from events_eventparticipant where event_id = %s)
                            select bp.id as pid, bp.center_id as home_center_id, ed.center_id as event_center_id, 
                                        ed.event_code, epd.max_id 
                            from base_participant bp, event_data ed, epd
                            where bp.id = ANY(%s)'''
    with connection.cursor() as cursor:
        cursor.execute(participant_query, [req_data['event_id'], req_data['event_id'], participant_ids])
        records = cursor.fetchall()
        
    return Response([])