from django.urls import path
from . import views

urlpatterns = [
    path('sendmsg/',views.send_message.as_view(), name="user_details" ),
    path('call/',views.make_call, name="make_call" ),
    # path('token/',views.generate_token, name="token" ),
    path('vedio/',views.make_video_call.as_view(), name="vedio_call" ),
    path('zoom/',views.meke_zoom_meeting, name="zoom_meeting" ),
]
