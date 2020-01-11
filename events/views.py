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

from django.conf import settings
from collections import defaultdict
from events import tasks


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
    
    permission_classes = (IsAuthenticatedOrPostOnly,)
    queryset = EventParticipant.objects.all()
    queryset = queryset.prefetch_related('participant')
    serializer_class = EventParticipantSerializer
    filter_fields = ['id', 'event', 'participant', 'registration_no', 'home_center', 'event_center', 'accommodation',
     'payment_status', 'cashier', 'big_buddy', 'role', 'registration_status', 'created_on', 'updated_on']

@api_view(['POST'])
def bulk_register(request):
    tasks.bulk_registeration.delay(request.data)
    # req_data = request.data
    # event_code = 'EVENT_{}'.format(req_data['event_id'])
    # if(settings.REDIS_CLIENT.exists(event_code) != 1):    
    #     with connection.cursor() as cursor:
    #         max_id_query = '''(select max(split_part(registration_no, '-', 4)::numeric) as max_id 
    #                             from events_eventparticipant where event_id = %s)'''
    #         cursor.execute(max_id_query,[req_data['event_id']])
    #         max_id_record = cursor.fetchall()
    #         settings.REDIS_CLIENT.set(event_code,max_id_record[0][0] or 1)    

    # d = defaultdict(list)
    # for r in req_data['participant_list']:
    #     d[r['id']] = [r['accommodation'], r['role']]

    # participant_ids = [c['id'] for c in req_data['participant_list']]

    # participant_query = '''with event_data as 
    #                             (select center_id, event_code from events_event where id = %s)
    #                         select bp.id as pid, bp.center_id as home_center_id, ed.center_id as event_center_id, 
    #                                     ed.event_code 
    #                         from base_participant bp, event_data ed
    #                         where bp.id = ANY(%s)'''

    # with connection.cursor() as cursor:
    #     cursor.execute(participant_query, [req_data['event_id'], participant_ids])
    #     participant_records = cursor.fetchall()
    #     participant_input_query = '''INSERT INTO EVENTS_EVENTPARTICIPANT ( 
    #                                                         registration_no,
    #                                                         accommodation,
    #                                                         payment_status,
    #                                                         amount_paid,
    #                                                         cashier,
    #                                                         big_buddy,
    #                                                         goal_achievement,
    #                                                         role ,
    #                                                         event_id,
    #                                                         event_center_id,
    #                                                         home_center_id,
    #                                                         participant_id,
    #                                                         registration_status ,
    #                                                         created_on,
    #                                                         updated_on,
    #                                                         skill
    #                                             ) VALUES(%s,%s,false,0,'','','',%s,
    #                                                             %s,%s,%s,%s,0,current_timestamp,current_timestamp,'')'''
    #     for participant  in participant_records:
    #         # print('ID:: ', participant[0])
    #         # print('D::',d)
    #         # print('from[]', d[participant[0]])
    #         # print(d.get(participant[0]))         
    #         cursor.execute(participant_input_query,[
    #             participant[3] + '-M-{}'.format(settings.REDIS_CLIENT.incr(event_code)),
    #             d.get(participant[0])[0],
    #             d.get(participant[0])[1],
    #             req_data['event_id'],
    #             participant[2],
    #             participant[1],
    #             participant[0]
    #         ])




    return Response([])
