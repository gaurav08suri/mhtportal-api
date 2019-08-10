from django.conf.urls import url
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from events.views import (EventViewSet,EventCategoryViewSet,
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


    url(r'^event-categories/(?P<pk>[0-9]+)/$', EventCategoryViewSet.as_view(api_endpoints_retrieve_update), name='events-categories-update'),

    url(r'^event-categories/$', EventCategoryViewSet.as_view(api_endpoints_list_create), name='events-categories-create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
