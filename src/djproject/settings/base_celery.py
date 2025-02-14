# Celery settings
from datetime import timedelta

from celery.schedules import crontab

from .base_django import TIME_ZONE, USE_TZ

# For RabbitMQ
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# See http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#time-zones
# celery timezone: the time zone specified in the TIME_ZONE setting will be used
if USE_TZ:
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = TIME_ZONE

# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_DISABLE_RATE_LIMITS = True
CELERY_WORKER_DISABLE_RATE_LIMITS = CELERY_DISABLE_RATE_LIMITS
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_HIJACK_ROOT_LOGGER = CELERYD_HIJACK_ROOT_LOGGER

CELERY_BEAT_SCHEDULE = {
    # 'task-clean_sessions': {
    #     'task': 'bs_room_support.tasks.clean_sessions',
    #     'schedule': crontab(hour=0, minute=5),
    # },
}
