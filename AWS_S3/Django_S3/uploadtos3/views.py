from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from s3 import functions

# image upload api
class upload_to_s3(APIView):
    # post request to upload files as form data
    def post(self,request):
        try:
            # get files from form 
            files = request.FILES.getlist('image')
            if files:
                urls = []
                for file in files:
                    print(f"before {file.name} - {file.size}")
                    # compress the image
                    image = functions.compress_image(file)

                    # upload file function returns file url
                    file_url = functions.upload_file_to_s3(image)
                    urls.append(file_url)
                    # store file url to uplodes model
                    # uploads.objects.create(img_url=file_url)
                return Response({"image_url": urls}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Status":"Error","error": str(e)})
        
#Read files from s3 bucket using file_url API
class read_from_s3(APIView):
     def get(self,request):
        # return Response({"status":"done"})         

        # get file url from query params
        file_url = request.query_params.get('file_url')
        # call the retrive file function
        file = functions.read_file_from_s3(file_url)
        # Save the file locally
        with open("downloaded_file.jpg", "wb") as f:
            f.write(file)
    
        return FileResponse(open("downloaded_file.jpg",'rb'),as_attachment=True)

class compress_file(APIView):

    def post(self,request):
        if request.method == 'POST':
            # get file from form data
            uploaded_file = request.FILES
            image_file = uploaded_file.get('image')
            orijinal_size = image_file.size
            # call the compress image function
            comp_image = functions.compress_image(image_file)

            return Response({"original":orijinal_size,"compressed":comp_image.tell()})         

