from email_task import send_mail,send_mail__to_multi_users
from celery import Celery
from datetime import datetime, timedelta
reciever_list = ['parasuram.k@datayaan.com',
                 'parasurambarath@gmail.com'
                #  'vishalakshi.k@medyaan.com'
                 ]
# task = send_mail__to_multi_users.apply_async(args=(reciever_list,),task_id='send mail to 2 mails')
# print(">>>>>",task.id)

# for to_mail in reciever_list:
#     task = send_mail.apply_async(args=(to_mail,),
#                                  task_id=f'send mail to {to_mail}',
#                                  eta=datetime.utcnow()+timedelta(minutes=2))    
#     print(">>>>>",task.id)