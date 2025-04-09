from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import user
from django.conf import settings
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
import base64
import requests


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

class send_message(APIView):
    def post(self, request):
        data = request.data
        user_name = data.get('username')
        phone = data.get('phone')
        obj = user(name=user_name, phonenumber=phone)
        obj.save()

        message = client.messages.create(
            from_=settings.TWILIO_PHONE_NUMBER,
            to=obj.phonenumber,
            body="hi parasuram, This is a test message from twilio",
            
        )
        data = {
            "msg_status":message.status,
            "msg_sid":message.sid,
            "msg_sid":message.price,
        }
        return Response({"status":"success","message":"user created succesfully","data":data}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def make_call(request):
    try:
        from_num = settings.TWILIO_PHONE_NUMBER
        to_num = request.data.get('to_num')

        if not to_num or len(to_num)!=10:
            return Response({"message":"Enter a valid phone number"}, status=status.HTTP_400_BAD_REQUEST)
        
        to_num = f"+91{to_num}"
        twiml = f'''
        <Response>
            <Say voice="man">vanakkamda mapla theniyila irunthu...!</Say>
        </Response>
        '''

        call = client.calls.create(
            from_=from_num,
            to=to_num,
            twiml=twiml
        )
        call_id = call.sid

        return Response({"status":"success","message":"Call initiated...!","call_id":to_num}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"status":"Error","Error":str(e)}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
def generate_token(identity, room):
    user_name = identity
    room_name = room
    token = AccessToken(
        account_sid=settings.TWILIO_ACCOUNT_SID,
        signing_key_sid=settings.TWILIO_API_KEY,
        secret=settings.TWILIO_API_SECRET,
        identity=user_name,
        )

    video_grant = VideoGrant(room=room_name)
    token.add_grant(video_grant)

    return token.to_jwt()

class make_video_call(APIView):
    def get(self, request):
        identity = request.query_params.get('identity')
        room = 'Test-room'
        token = None
        if identity:
            token = generate_token(identity, room)
            context = {
                "identity":identity,
                "room":room,
                "token":token
            }
            return render(request, "index.html", context)
        return render(request, "index.html")

# make request for zoom_token to zoom developer api
def get_zoom_token():
    # O Auth token api from Zoom API Docs
    url = "https://zoom.us/oauth/token"
    # credentials provided by zoom app
    credentials = f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization" : f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        "grant_type" : "account_credentials",
        "account_id" : settings.ZOOM_ACC_ID
    }
    # make a post request to zoom developer api with headers and parameters
    response = requests.post(url=url, headers=headers, params=params)
    # return zoom token 
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Zoom Token Error: ", response.text)

# function for create Zoom meeting URl
@api_view(['POST'])
def meke_zoom_meeting(request):
    try:
        # get zoom token
        token = get_zoom_token()
        # api to create a meeting - Zoom API Docs
        url = f"https://api.zoom.us/v2/users/{settings.ZOOM_USER_ID}/meetings"
        headers = {
            "Authorization" : f"Bearer {token}",
            "Content-Type" : "application/json"
        }
        
        meeting_details = {
            "topic": "Video Call Meeting",
            "type": 1, # 1-Instant Meeting, 2-Scheduled, 3,8-Recurring Meeting
            "password":"welcome",
            "settings": {
                "host_video": False,
                "participant_video": True,
                "mute_upon_entry": True,
                "approval_type": 1, # 0: Auto-approve, 1: Manually approve, 2: No registration
                "waiting_room": True,
                "join_before_host": True
            }
        }
        # make a post request create_meeting api with headers and parameters
        response = requests.post(url=url, headers=headers, json=meeting_details)
        meeting_data = response.json()
        # return meeting_url, password from response 
        data = {
            "meeting_name":meeting_details['topic'],
            "meeting_id":meeting_data['id'],
            "join_URL":meeting_data['join_url'],
            "password":meeting_data['password']
        }
        return Response({"meeting_data":data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"message":"Error occured","Error":str(e)})