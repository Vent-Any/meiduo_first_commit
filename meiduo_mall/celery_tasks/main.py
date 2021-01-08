from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')


app = Celery('celery_tasks')
app.config_from_object('celery_tasks.config')
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])