from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from base.models import (Address, Center, Participant)



class Event(models.Model):
    """Event represents an particular Event.

    venue field is an foreign key to :model: `base.Address`
    """

    # Validators
    ONLY_DIGITS_VALIDATOR = RegexValidator(regex=r'^[0-9]*$',
                                message="Only digits allowed.")

    name = models.CharField(max_length=50, help_text=_("Event Name"))
    venue = models.ForeignKey(Address, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='center',
                                help_text=_("Center"))
    start_date = models.DateField(help_text=_("Event Start Date"))
    end_date = models.DateField(help_text=_("Event End Date"))
    last_date_of_registration = models.DateField(
                                help_text=_("Last Date of Registration"))
    fees = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text=_("Event Fees"))
    late_fees = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text=_("Late Registration Fees"))
    accommodation_provided = models.BooleanField(help_text=_("Is Accommodation Provided?"))

    # This represents Age group
    min_age = models.CharField(max_length=2, validators=[ONLY_DIGITS_VALIDATOR,],
                                help_text=_("Age Group Lower limit"))
    max_age = models.CharField(max_length=2, validators=[ONLY_DIGITS_VALIDATOR,],
                                help_text=_("Age Group Upper limit"))

    rules = models.TextField(help_text=_("Any Rules"), blank=True)
    remarks = models.TextField(help_text=_("Any Remarks"), blank=True)



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
    ONLY_ALPHANUMERIC_VALIDATOR = RegexValidator(regex=r'^[0-9 a-z A-Z]*$',
                                message="Only digits allowed.")

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    pariticipant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=20, validators=[ONLY_ALPHANUMERIC_VALIDATOR,],
                                        help_text=_("Registration Number"))
    home_center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='home_center',
                                    help_text=_("Home Center"))
    event_center = models.ForeignKey(Center, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='event_center', help_text=_("Event Center"))
    accommodation = models.BooleanField(help_text=_("Is Accommodation Required?"))
    payment_status = models.BooleanField(help_text=_("Has paid?"))
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Amount Paid"))
    cashier = models.CharField(max_length=50, help_text=_("Cashier"))
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, help_text=_("Role"))



