from django.conf.urls import url
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from events.views import (EventViewSet,
                        EventParticipantViewSet)

api_endpoints_retrieve_update = {
    'get': 'retrieve',
    'patch': 'partial_update',
    }
if settings.DEBUG:
    api_endpoints_retrieve_update['delete'] = 'destroy'

api_endpoints_list_create = {
    'get': 'list',
    'post': 'create',
    }

urlpatterns = [
    url(r'^event-participants/(?P<pk>[0-9]+)/$', EventParticipantViewSet.as_view(
        api_endpoints_retrieve_update), name='event-participants-retrieve-update'),

    url(r'^event-participants/$', EventParticipantViewSet.as_view(api_endpoints_list_create),
        name='event-participants-list-create'),

    url(r'^(?P<pk>[0-9]+)/$', EventViewSet.as_view(api_endpoints_retrieve_update), name='events-retrieve-update'),

    url(r'^$', EventViewSet.as_view(api_endpoints_list_create), name='events-list-create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
