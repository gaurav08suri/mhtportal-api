import os
import sys
import django
sys.path.append('/code/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mhtportal.settings")
from django.conf import settings
django.setup()

def main():

    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group
    from django.core.exceptions import MultipleObjectsReturned
    from base.models import (Profile, Center)
    import csv

    csvfile = open('profiles.csv', 'r')
    reader = csv.reader(csvfile,)
    all_profiles = User.objects.all()
    for row in reader:
        print("Creating/Updating Profile/User with data {}".format(row))
        try:
            c = Center.objects.get(id=row[5])
        except Center.DoesNotExist:
            print("Don't know what to do here")
            print("No Center with id {}".format(row[5]))
            exit(-1)

        username = '{}_{}'.format(row[5], row[1][:5])
        password = 'admin@{}#'.format(username)
        try:
            u, _ = User.objects.get_or_create(
                username=username, first_name=username, password=password)
        except MultipleObjectsReturned:
            print("Don't know what to do here")
            print("multiple users returned")
            exit(-1)
        print(u)
        u.is_active = True
        u.is_staff = False
        # user.groups = Group.objects.filter(name = row[5])

        try:
            profile, _ = Profile.objects.get_or_create(
                user=u,
                center=c,
                gender=row[0],
                mobile=row[1],
                min_age=row[2],
                max_age=row[3],
            )
        except MultipleObjectsReturned:
            print("Don't know what to do here")
            print("multiple profiles returned")
            exit(-1)

        c.save()
        profile.save()
        u.save()




if __name__ == "__main__":
    main()