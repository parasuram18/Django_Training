from datetime import datetime,timedelta
to_mail = 'parasuram.k@datayaan.com'
name = to_mail.split('@')[0]
print(name)

date = datetime(2025, 3, 24,11,5)
print(date)
print(datetime.utcnow()+timedelta(minutes=2))