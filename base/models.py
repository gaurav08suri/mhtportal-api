from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from localflavor.in_.in_states import STATE_CHOICES
import string


class Center(models.Model):
    """Center represents an Ymht Center
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return "Center: {}".format(name)


    def save(self, *args, **kwargs):
        """Filter fields before save

        Strip trailing whitespaces and comma characters from name field.
        convert to lowercase
        """

        self.name = self.address_1.rstrip(string.whitespace+',').lower()
        super().save(*args, **kwargs)



class Address(models.Model):
    """Address represents an Event Address
    """

    # Validators
    ONLY_DIGITS_VALIDATOR = RegexValidator(regex=r'^[0-9]*$',
                                message="Only digits allowed.")

    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=30, choices=STATE_CHOICES)
    country = CountryField()
    zip_code = models.CharField(max_length=6, validators=[ONLY_DIGITS_VALIDATOR,])
    raw = models.TextField(blank=True)

    def __str__(self):
        return "Address: {}".format(raw)

    def save(self, *args, **kwargs):
        """Filter fields before save

        Strip trailing whitespaces and comma characters from address fields.
        build raw field to represent complete address as a string
        """

        self.address_1 = self.address_1.rstrip(string.whitespace+',')
        self.address_2 = self.address_1.rstrip(string.whitespace+',')
        self.city = self.address_1.rstrip(string.whitespace+',')
        self.raw = '{}\n,{}\n,{}-{}\n,{}\n,{}'.format(
                address_1, address_2, city, state, country, zip_code)

        super().save(*args, **kwargs)



class Participant(models.Model):
    """Pariticpant represents an profile of event pariticipant

    center field is an foreign key to :model: `base.Center`
    """

    # Choices
    GENDER_FEMALE = 'male'
    GENDER_MALE = 'female'
    GENDER_CHOICES = (
            (GENDER_FEMALE, 'Female'),
            (GENDER_MALE, 'Male'))

    # Validators
    MOBILE_VALIDATOR = RegexValidator(regex=r'^\+?1?\d{9,15}$',
            message="Mobile Number must be entered in the format:\
                    '+999999999999'. Up to 15 digits allowed.")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    mobile = models.CharField(max_length=15, validators=[MOBILE_VALIDATOR,])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                                default=GENDER_MALE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)

    # Currently we are keeping this field optional
    email = models.EmailField(blank=True)
    guardian_name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Participant: {} {}\n {}".format(
                first_name, last_name, center)



class Profile(models.Model):
    """Profile represents users who would have access to frontend admin dashboard
    user field is an OneToOne Field with :model:`auth.User`
    center field is an foreign key to :model:`base.Center`

    """

    # Choices
    GENDER_FEMALE = 'male'
    GENDER_MALE = 'female'
    GENDER_CHOICES = (
            (GENDER_FEMALE, 'Female'),
            (GENDER_MALE, 'Male'))

    # Validators
    MOBILE_VALIDATOR = RegexValidator(regex=r'^\+?1?\d{9,15}$',
            message="Mobile Number must be entered in the format:\
                    '+999999999999'. Up to 15 digits allowed.")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                                default=GENDER_MALE)
    mobile = models.CharField(max_length=15, validators=[MOBILE_VALIDATOR,], blank=True)
    # age_group



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Profile when the User is created."""

    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Profile when the User is modified"""
    instance.profile.save()



