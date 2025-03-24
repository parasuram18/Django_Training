from celery import shared_task
import time
from django.core.mail import send_mail



@shared_task
def add(a,b):
    print("start")
    time.sleep(10)
    ans = a+b
    print("end")
    return "task completed"


@shared_task
def send_mail_to(to_mail):
    subject = 'Task summary(20-03-2025)'
    message = "Hi team , Please find my task details today..."
    from_mail = 'parasuramech@gmail.com'
    
    send_mail(subject=subject, message=message, from_email=from_mail, recipient_list=[to_mail],fail_silently=True)
    
    return "mail sent succesfully"