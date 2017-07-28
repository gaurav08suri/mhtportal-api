from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from events.views import (EventViewSet,
                        EventParticipantViewSet)



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
    url(r'^event-participants/(?P<pk>[0-9]+)/$', EventParticipantViewSet.as_view(
        api_endpoints_default), name='event-participants'),

    url(r'^event-participants/list/$', EventParticipantViewSet.as_view(api_endpoints_list),
        name='event-participants-list'),

    url(r'^list/$', EventViewSet.as_view(api_endpoints_list), name='events-list'),

    url(r'^(?P<pk>[0-9]+)/$', EventViewSet.as_view(api_endpoints_default), name='events'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
