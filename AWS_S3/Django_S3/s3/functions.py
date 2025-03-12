from django.http import FileResponse
import boto3
from django.conf import settings
from django.core.files.storage import default_storage
import time,os,io
from PIL import Image
def upload_file_to_s3(file):

    # create a s3 session with credentials
    # session = boto3.Session(
    #     aws_access_key_id=settings.AWS_ACCESS_KEY,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS,
    #     region_name=settings.AWS_REGION
    #     )
    # create client connects t s3 bcket
    # s3_client = session.client('s3')
    # store files to temporary storage
    temp_file_path = default_storage.save(f'static/images/{file.name}',file)
    # local file path to upload_file method
    local_path = default_storage.path(temp_file_path)
    # get bucket name from settings 
    # Bucket_name=settings.AWS_STORAGE_BUCKET_NAME
    # s3 storage file path - fole to be uploadedin this path
    s3_key = f"{settings.AWS_STORAGE_FOLDER_NAME}/{int(time.time())}_{file.name}"

    # call upload_file method 
    # s3_client.upload_file(
    #     Filename=local_path,
    #     Bucket = Bucket_name,
    #     Key=s3_key,
    #     ExtraArgs={"ACL": "public-read", "ContentType": file.content_type})
    
    # file_data = file.read()
    # s3_client.put_object(
    #     Bucket=Bucket_name,
    #     Key=f"{settings.AWS_STORAGE_FOLDER_NAME}/{time.time()}_image.jpg",
    #     Body=file_data,
    #     ACL="public-read",
    #     ContentType="image/jpeg")
    
    file_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_key}"
    if os.path.exists(local_path):
        os.remove(local_path)

    return file_url

def read_file_from_s3(file_url):
    # create a s3 session with credentials
    session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS,)
    # Create an S3 client
    s3_client = session.client("s3")
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    # Extract bucket name and file key 
    file_key = '/'.join(file_url.split('/')[-2:]) #"medyaan_dev/1741258608_mayilirage.jpg"
    # Retrieve the object from bucket storage
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    # Read the content
    file_content = response["Body"].read()

    return file_content

def compress_image(file):
    # set maximum size upto 1MB
    max_size = 1*1024*1024
    orijinal_size = file.size
     # check image size
    if orijinal_size <= max_size:
        return file
    # if image_size > max_size:
    # create on memmory io file for saving
    file_name = file.name
    image = Image.open(file)
    # get image's original format
    original_format = image.format
    output = io.BytesIO()
    # start compression
    quality = 95
    image.save(fp=output,format=original_format,quality = quality,optimize = True)
    compressed_size = output.tell()
    # if image_size > max_size:
    while compressed_size >= max_size or quality <= 10:
        # read from top
        output.seek(0)
        # empty output file
        output.truncate(0)
        # reduce quality-5%
        image.save(fp=output,format=original_format,quality = quality,optimize = True)
        # size of the file after compressed 
        compressed_size = output.tell()
        quality-=5
    print(f"after {file.name} - {compressed_size}")
    output.name = file_name
    return output

    # file_name = image.name
    # img = Image.open(image)
    # output = io.BytesIO()
    # img.save(output,format='JPEG',quality=50,optimize=True)
    # output.name = file_name

    # print(img.mode)
    # print(img.size)
    # print(img.format)
    # size=(40,40)
    # r_img= img.resize(size)
    # print(img.size)
    return output
