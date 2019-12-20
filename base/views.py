from django.shortcuts import get_object_or_404
from django_countries import countries
from localflavor.in_.in_states import STATE_CHOICES

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from base.models import (Center,
                        CenterScope,
                        ScopedCenter,
                        Address,
                        Participant,
                        Profile)
from base.serializers import (AddressSerializer,
                            CenterSerializer,
                            CenterScopeSerializer,
                            ScopedCenterSerializer,
                            ParticipantSerializer,
                            ProfileSerializer)

from events.tasks import test

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object



class MeView(APIView):
    """
    Display Profile of current logged in User.

    * Requires authentication.
    * Only logged in users are able to access this view.
    """
    #permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return Profile of current logged in user.
        """
        test.delay("1")
        #profile = get_object_or_404(Profile, user=request.user)
        #ps = ProfileSerializer(profile)
        return Response(None)

class CountriesView(APIView):

    def get(self, request, format=None):
        return Response(dict(countries))

class StatesView(APIView):
    
    def get(self, request, format=None):
        return Response(dict(STATE_CHOICES))

class CenterViewSet(ModelViewSet):
    """This endpoint Represents the Centers

    It presents the list of Current Centers.
    """
    @method_decorator(cache_page(60*60*2))
    def list(self, request, *args, **kwargs):
        super(CenterViewSet, self).list(request, *args, **kwargs)

    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    filter_fields = ['id', 'name', 'parent', 'is_displayed']



class CenterScopeViewSet(ModelViewSet):
    """This endpoint Represents the Center Scopes

    It presents the list of Current Center Scopes.
    """
    queryset = CenterScope.objects.all()
    serializer_class = CenterScopeSerializer



class ScopedCenterViewSet(ModelViewSet):
    """This endpoint Represents the Centers with definite Scopes

    It presents the list of Current Centers with definite Scopes
    """
    queryset = ScopedCenter.objects.all()
    serializer_class = ScopedCenterSerializer



class AddressViewSet(ModelViewSet):
    """This endpoint Represents the Event Addresses

    It presents the address for the given event
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_fields = ['id', 'city', 'state', 'country', 'zip_code']



class ParticipantViewSet(ModelViewSet):
    """This endpoint Represents the Participants

    It can create/update/retrieve an Participant
    It also presents lists of Participants
    """
    
    permission_classes = (IsAuthenticated,)
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    filter_fields = ['id', 'first_name', 'last_name', 'date_of_birth' 'gender',
    'center', 'other_center', 'email']



class ProfileViewSet(ModelViewSet):
    """This endpoint Represents the Profiles in the system

    It can create/update/retrieve an Profile
    It also presents lists of Profiles
    """
    permission_classes = (IsAuthenticated,)

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_fields = ['id', 'user', 'center', 'gender', 'min_age', 'max_age']


