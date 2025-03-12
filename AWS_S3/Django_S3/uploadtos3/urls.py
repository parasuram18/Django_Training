from django.urls import path
from . import views

urlpatterns = [
    path('uploadfile/',views.upload_to_s3.as_view(),name='upload_image'),
    path('readfile/',views.read_from_s3.as_view(),name='read_image'),
    path('compress/',views.compress_file.as_view(),name='compress_image')
]
