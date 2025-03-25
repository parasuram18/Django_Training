from celery import Celery,shared_task
import smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import eventlet, time
from datetime import datetime, timedelta
from celery.schedules import crontab


app = Celery(
    'email_task',
    broker= 'redis://127.0.0.1:6379/0',
    backend = 'redis://127.0.0.1:6379/0'
)

app.conf.update(
    worker_concurrency=4,
    broker_connection_retry_on_startup = True
)
app.conf.timezone = 'UTC'



EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'parasuramech@gmail.com'
EMAIL_HOST_PASSWORD = 'zjlkwwxvjxxmybsb'


@app.task
def send_mail(to_mail):
    start = time.time()
    message = MIMEMultipart()
    message['From'] = EMAIL_HOST_USER
    message['To'] = to_mail
    message['Subject'] = f'Task Mail{time.time()}'
    name = to_mail.split('@')[0]
    body = f"Hi {name} , This is the test mail from Parasuram..."
    message.attach(MIMEText(body,'plain'))
    
    session = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
    session.starttls()
    session.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)

    session.sendmail(from_addr=EMAIL_HOST_USER,to_addrs=to_mail,msg=message.as_string())
    session.quit()
    end = time.time()
    
    return f"mail sent to {name} succesfully in {end-start} seconds"


@shared_task
def send_mail__to_multi_users(reciever_list):
    result = {}
    for to_mail in reciever_list:
        # time.sleep(30)
        message = MIMEMultipart()
        message['From'] = EMAIL_HOST_USER
        message['To'] = to_mail
        message['Subject'] = f'Task Mail{time.time()}'
        name = to_mail.split('@')[0]
        body = f"Hi {name} , This is the test mail from Parasuram..."
        message.attach(MIMEText(body,'plain'))

        session = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
        session.starttls()
        session.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)
        session.sendmail(from_addr=EMAIL_HOST_USER,to_addrs=to_mail,msg=message.as_string())
        session.quit()
        result[to_mail]=f"mail sent to {name} succesfully"
    return result

app.conf.beat_schedule = {
    "run_every_60_seconds":{
        'task':'email_task.send_mail',
        'schedule':timedelta(seconds=1),
        'args':['Krishnakuamri.g@medyaan.com',]
    }
}
# app.conf.timezone = 'Asia/Kolkata'  # Set the correct timezone
# # app.conf.timezone = 'UTC'

# app.conf.beat_schedule = {
#     "send_daily_email":{
#         'task':'email_task.send_mail',
#         'schedule':crontab(hour=19, minute=3),
#         'args':['parasuram.k@datayaan.com',]
#     }
# }
