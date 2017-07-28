from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from base.views import (CenterView,
                        AddressView,
                        ParticipantViewSet,
                        ProfileViewSet)

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
    url(r'^addressess/(?P<pk>[0-9]+)/$', AddressView.as_view(),
        name='addressess'),

    url(r'^participants/(?P<pk>[0-9]+)/$', ParticipantViewSet.as_view(
        api_endpoints_default), name='participants'),

    url(r'^profiles/(?P<pk>[0-9]+)/$', ProfileViewSet.as_view(
        api_endpoints_default), name='profiles'),

    url(r'^participants/list/$', ParticipantViewSet.as_view(
        api_endpoints_list), name='participants-list'),

    url(r'^profiles/list/$', ProfileViewSet.as_view(api_endpoints_list),
        name='profiles-list'),

    url(r'^centers/$', CenterView.as_view(), name='centers'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
