from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time, threading
from . import uploadf



class update_excel(APIView):
    def post(self,request):
        
        start = time.time()
        # get file from form data
        file = request.FILES.get('file')
        
        # df = pd.read_excel(file)
        # create new thread
        thread1 = threading.Thread(target=uploadf.upload_to_db,args=(file,))
        # run the thread in background
        thread1.start()

        end = time.time()
        # success response message
        message= 'file upload succesfully'
        return Response({'message':message,'time':end-start},status=status.HTTP_200_OK)

