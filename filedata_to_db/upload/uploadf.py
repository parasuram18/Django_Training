from .models import speciality_master
import pandas as pd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.utils import timezone

# function to save the file in local storage
def save_to_default_storage(file):
    # default storage path
    file_name = f"uploads/files/{file.name}"
    # store file in default storage
    file = default_storage.save(name=file_name, content=ContentFile(file.read()))
    # get the absolute file path
    file_path =  default_storage.path(file)
    
    return file_path


def upload_to_db(file):
    # save the file in local storage
    file_path = save_to_default_storage(file)
    print(">>>>>",file_path)
    
    # alternative method if the file was already stored in local storage
    # file_path = f'uploads/files/{file.name}'
    
    # check file extension for handle files
    if file.name.endswith('.xlsx'):
        # create dataframe - have all the datas in list format 
        df = pd.read_excel(file_path)
    elif file.name.endswith('.csv'):    
        df = pd.read_csv(file_path)
        
    # convert timezone for upload datetime datas
    # df["Date of Registration"] = pd.to_datetime(df["Date of Registration"]).apply(timezone.make_aware)
    
    # iterate through each row in file
    for row in df.values:
        # map db fields and excel columns
        
        # finance.objects.create(field1=row[0], field2=row[1], field3=row[2], field4=row[3])
        # hosphital_details.objects.create(hosphital_id=row[0], name=row[1], location=row[2], city=row[3], registered_date=row[4])
        speciality_master.objects.create(speciality_desc=row[3],speciality_amount=row[4],speciality_currency=row[5],speciality_currency_symbol=row[6],created_by=row[7],modified_by=row[9],iu_id_id=row[11])
    
    # after processing data remove file from default storage 
    if os.path.exists(file_path):
        os.remove(file_path)
