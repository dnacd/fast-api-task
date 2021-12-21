import os
from celery import Celery

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery = Celery("celery", broker=broker_url, result_backend=result_backend)

# celery.conf.task_routes = {
#     "plus_task": {'queue': 'main-queue'}
# }
