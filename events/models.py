from django.db import models
from django.core.validators import RegexValidator
from base.models import (Address, Center, Participant)


class Event(models.Model):
    """Event represents an particular Event.

    venue field is an foreign key to :model: `base.Address`
    """

    # Validators
    ONLY_DIGITS_VALIDATOR = RegexValidator(regex=r'^[0-9]*$',
                                message="Only digits allowed.")

    name = models.CharField(max_length=50)
    venue = models.ForeignKey(Address, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    last_date_of_registration = models.DateField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    late_fees = models.DecimalField(max_digits=10, decimal_places=2)

    # This represents Age group
    min_age = models.CharField(max_length=2, validators=[ONLY_DIGITS_VALIDATOR,])
    max_age = models.CharField(max_length=2, validators=[ONLY_DIGITS_VALIDATOR,])
    remarks = models.TextField()

class EventParticipant(models.Model):
    """EventParticipant stores information about an participant for the Event.

    The EventParticipant table contains information about an event participant
    for an event.
    event field is an foreign key to :model: `events.Event`
    pariticipant field is an foreign key to :model: `base.Pariticpant`
    home_center field is an foreign key to :model: `base.Center`
    event_center field is optional and an foreign key to :model: `base.Center`
    """

    # Choices
    ROLE_PARTICIPANT = 'pariticipant'
    ROLE_HELPER = 'helper'
    ROLE_COORDINATOR = 'coordinator'
    ROLE_CHOICES = (
            (ROLE_PARTICIPANT, 'Participant'),
            (ROLE_HELPER, 'Helper'),
            (ROLE_COORDINATOR, 'Coordinator'))

    # Validators
    ONLY_DIGITS_VALIDATOR = RegexValidator(regex=r'^[0-9]*$',
                                message="Only digits allowed.")

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    pariticipant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=20, validators=[ONLY_DIGITS_VALIDATOR,])
    home_center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='home_center')
    event_center = models.ForeignKey(Center, on_delete=models.CASCADE, blank=True,
                                    null=True, related_name='event_center')
    accommodation = models.BooleanField()
    payment_status = models.BooleanField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    cashier = models.CharField(max_length=50)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)



