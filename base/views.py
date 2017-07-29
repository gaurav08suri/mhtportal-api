from rest_framework.viewsets import ModelViewSet
# from rest_framework.generics import (RetrieveAPIView,
#                                     ListAPIView)
from base.models import (Center,
                        Address,
                        Participant,
                        Profile)
from base.serializers import (AddressSerializer,
                            CenterSerializer,
                            ParticipantSerializer,
                            ProfileSerializer)



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



class CenterViewSet(ModelViewSet):
    """This endpoint Represents the Centers

    It presents the list of Current Centers.
    """
    queryset = Center.objects.all()
    serializer_class = CenterSerializer



class AddressViewSet(ModelViewSet):
    """This endpoint Represents the Event Addresses

    It presents the address for the given event
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer



class ParticipantViewSet(ModelViewSet):
    """This endpoint Represents the Participants

    It can create/update/retrieve an Participant
    It also presents lists of Participants
    """
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer



class ProfileViewSet(ModelViewSet):
    """This endpoint Represents the Profiles in the system

    It can create/update/retrieve an Profile
    It also presents lists of Profiles
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



