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
    from base.models import Profile

    for u in User.objects.all():
        print("Changing User password for {}".format(u))
        password = 'admin@{}#'.format(u.username)
        u.set_password(password)
        u.save()
        print("New Password is {}".format(password))



if __name__ == "__main__":
    main()