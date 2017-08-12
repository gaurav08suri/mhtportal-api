import os
import logging
from celery import Celery



logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mhtportal.settings')

app = Celery('mhtportal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    logger.info('Request: {0!r}'.format(self.request))