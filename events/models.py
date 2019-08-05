import datetime
from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from base.models import (Address, Center, Participant)

class EventCategory(models.Model):
    category = models.CharField(max_length=50, default="", help_text=_("Event Category"))

    def __str__(self):
        return "Event Category: {}".format(self.category)



class Event(models.Model):
    """Event represents an particular Event.

    venue field is an foreign key to :model: `base.Address`
    """

    # Choices
    YEAR_CHOICES = []
    curr_year = datetime.datetime.now().year
    for r in range(curr_year, curr_year+5):
        YEAR_CHOICES.append((r,r))

    GENDER_FEMALE = 'female'
    GENDER_MALE = 'male'
    GENDER_CHOICES = (
            (GENDER_FEMALE, 'Female'),
            (GENDER_MALE, 'Male'))

    name = models.CharField(max_length=50, help_text=_("Event Name"))
    venue = models.ForeignKey(Address, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, help_text=_("Center"))
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, help_text=_("Event Category"), default="")
    year = models.PositiveIntegerField(choices=YEAR_CHOICES, default=curr_year,
                                help_text=_('year'))
    start_date = models.DateField(help_text=_("Event Start Date"))
    end_date = models.DateField(help_text=_("Event End Date"))
    last_date_of_registration = models.DateField(
                                help_text=_("Last Date of Registration"))
    fees = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text=_("Event Fees"))
    late_fees = models.DecimalField(max_digits=10, decimal_places=2,
                                help_text=_("Late Registration Fees"))
    accommodation_provided = models.BooleanField(help_text=_("Is Accommodation Provided?"))
    event_code = models.CharField(max_length=100, unique=True, help_text=_("Event Code"))
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    # This represents age-group
    min_age = models.PositiveIntegerField(help_text=_("Age Group lower limit"))
    max_age = models.PositiveIntegerField(help_text=_("Age Group Upper limit"))

    rules = models.TextField(help_text=_("Any Rules"), blank=True)
    remarks = models.TextField(help_text=_("Any Remarks"), blank=True)
    active = models.BooleanField(help_text=_("Is event active?"))



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
    ROLE_PARTICIPANT = 'participant'
    ROLE_HELPER = 'helper'
    ROLE_COORDINATOR = 'coordinator'
    ROLE_CHOICES = (
            (ROLE_PARTICIPANT, 'Participant'),
            (ROLE_HELPER, 'Helper'),
            (ROLE_COORDINATOR, 'Coordinator'))

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=100, unique=True, help_text=_("Registration Number"))
    home_center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name='home_center',
                                    help_text=_("Home Center"))
    event_center = models.ForeignKey(Center, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='event_center', help_text=_("Event Center"))
    accommodation = models.BooleanField(help_text=_("Is Accommodation Required?"))
    payment_status = models.BooleanField(help_text=_("Has paid?"))
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Amount Paid"))
    cashier = models.CharField(max_length=50, help_text=_("Cashier"), blank=True)
    big_buddy = models.CharField(max_length=50, help_text=_("Big Buddy"), blank=True)
    goal_achievement = models.CharField(max_length=100, help_text=_("Goal Achievement"), blank=True)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, help_text=_("Role"))
    registration_status = models.PositiveSmallIntegerField(default=0, help_text=_("Registration Status"))
    created_on = models.DateTimeField(auto_now_add=True, help_text=_("Event Participant Created on"))
    updated_on = models.DateTimeField(auto_now=True, help_text=_("Event Participant Updated on"))
    skill = models.TextField(blank=True, help_text=_("Skill"))


