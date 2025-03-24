from celery import Celery
from task import add

app = Celery(
    'task',
    broker= 'redis://localhost:6379/0',
    backend = 'redis://localhost:6379/0'
)
broker_connection_retry_on_startup = True
app.autodiscover_tasks()

result = add.delay(2,3)
print("------task_id :",result.id)