from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from events.views import (EventViewSet,
                        EventParticipantViewSet)



schema_view = get_schema_view(title='Events API')
api_endpoints_default = {
        'get': 'get',
        'post': 'post',
        'put': 'put',
        'patch': 'patch',
        }
api_endpoints_list = {
        'get': 'list',
        }

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', EventViewSet.as_view(api_endpoints_default), name='events'),
    url(r'^list/$', EventViewSet.as_view(api_endpoints_list), name='events-list'),
    url(r'^api-info/$', schema_view, name='api-info'),
    url(r'^event-participants/(?P<pk>[0-9]+)/$', EventParticipantViewSet.as_view(
        api_endpoints_default), name='event-participants'),
    url(r'^event-participants/list/$', EventParticipantViewSet.as_view(api_endpoints_list),
        name='event-participants-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
