import os
import sys
import django
sys.path.append('/code/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mhtportal.settings")
from django.conf import settings
django.setup()

def main():

    from base.models import (CenterScope,
                            ScopedCenter,
                            Center)

    cs = CenterScope.objects.get(gender='male', min_age=13, max_age=21)
    for c in Center.objects.all():
        print("Creating ScopedCenter for {} with {}".format(c, cs))
        try:
            sc, created= ScopedCenter.objects.get_or_create(center=c, center_scope=cs)
            if created:
                sc.save()
        except Exception as e:
            print("unable to create ScopedCenter")
            print("Error: {}".format(e))
            exit(-1)




if __name__ == "__main__":
    main()