from base.models import (Address,
                        Center,
                        Participant,
                        Profile)
from rest_framework.serializers import ModelSerializer
from django_countries.serializer_fields import CountryField



class CenterSerializer(ModelSerializer):
    """CenterSerializer serializes the Center model
    into json object and vice versa.
    """

    class Meta:
        model = Center
        exclude = ()



class AddressSerializer(ModelSerializer):
    """AddressSerializer serializes the Address model
    into json object and vice versa.
    """
    country = CountryField()
    
    class Meta:
        model = Address
        exclude = ()



class ParticipantSerializer(ModelSerializer):
    """PariticpantSerializer serializes the Participant model
    into json object and vice versa.
    """

    class Meta:
        model = Participant
        exclude = ()



class ProfileSerializer(ModelSerializer):
    """ProfileSerializer serializes the Profile model
    into json object and vice versa.
    """

    class Meta:
        model = Profile
        exclude = ()



