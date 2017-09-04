from django.conf.urls import url
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from base.views import (CenterViewSet,
                        CenterScopeViewSet,
                        ScopedCenterViewSet,
                        AddressViewSet,
                        ParticipantViewSet,
                        ProfileViewSet)

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
    url(r'^centers/(?P<pk>[0-9]+)/$', CenterViewSet.as_view(
        api_endpoints_retrieve_update),name='centers-retrieve-update'),

    url(r'^center-scopes/(?P<pk>[0-9]+)/$', CenterScopeViewSet.as_view(
        api_endpoints_retrieve_update),name='center-scopes-retrieve-update'),

    url(r'^scoped-centers/(?P<pk>[0-9]+)/$', ScopedCenterViewSet.as_view(
        api_endpoints_retrieve_update),name='scoped-centers-retrieve-update'),

    url(r'^addresses/(?P<pk>[0-9]+)/$', AddressViewSet.as_view(
        api_endpoints_retrieve_update), name='addressess-retrieve-update'),

    url(r'^participants/(?P<pk>[0-9]+)/$', ParticipantViewSet.as_view(
        api_endpoints_retrieve_update), name='participants-retrieve-update'),

    url(r'^profiles/(?P<pk>[0-9]+)/$', ProfileViewSet.as_view(
        api_endpoints_retrieve_update), name='profiles-retrieve-update'),

    url(r'^centers/$', CenterViewSet.as_view(
        api_endpoints_list_create),name='centers-list-create'),

    url(r'^center-scopes/$', CenterScopeViewSet.as_view(
        api_endpoints_list_create),name='center-scopes-list-create'),

    url(r'^scoped-centers/$', ScopedCenterViewSet.as_view(
        api_endpoints_list_create),name='scoped-centers-list-create'),

    url(r'^addresses/$', AddressViewSet.as_view(
        api_endpoints_list_create), name='addressess-list-create'),

    url(r'^participants/$', ParticipantViewSet.as_view(
        api_endpoints_list_create), name='participants-list-create'),

    url(r'^profiles/$', ProfileViewSet.as_view(api_endpoints_list_create),
        name='profiles-list-create'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
