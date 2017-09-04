from base.models import (Address,
                        Center,
                        CenterScope,
                        ScopedCenter,
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
        fields = '__all__'



class CenterScopeSerializer(ModelSerializer):
    """CenterScopeSerializer serializes the CenterScope model
    into json object and vice versa.
    """

    class Meta:
        model = CenterScope
        fields = '__all__'



class ScopedCenterSerializer(ModelSerializer):
    """ScopedCenterSerializer serializes the ScopedCenter model
    into json object and vice versa.
    """

    class Meta:
        model = ScopedCenter
        fields = '__all__'



class AddressSerializer(ModelSerializer):
    """AddressSerializer serializes the Address model
    into json object and vice versa.
    """
    country = CountryField()

    class Meta:
        model = Address
        fields = '__all__'



class ParticipantSerializer(ModelSerializer):
    """PariticpantSerializer serializes the Participant model
    into json object and vice versa.
    """

    class Meta:
        model = Participant
        fields = '__all__'



class ProfileSerializer(ModelSerializer):
    """ProfileSerializer serializes the Profile model
    into json object and vice versa.
    """

    class Meta:
        model = Profile
        fields = '__all__'



