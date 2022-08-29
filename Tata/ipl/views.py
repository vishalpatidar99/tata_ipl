from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
# Create your views here.
from django.core.mail import send_mail
from django.http import JsonResponse,HttpResponse
from .models import *
from Tata import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from .serializers import *
from datetime import date,datetime
# Create your views here.

def user_list(request):
    return render(request,'user_list.html',{'users':User.objects.all()})

# def user_details(request,id):
#     return render(request,'user_details.html',{'user ':User.objects.filter(id=id).first()})

def schedule(request):
    return render(request,'schedule.html',{})
def user_details(request,id):
    '''
    user detail based on id
    '''
    user = User.objects.filter(id=id).values()
    data = []
    dic={}
    dic["id"] = user[0]['id']
    dic["first name"] = user[0]['first_name']
    dic["last name"] = user[0]['last_name']
    dic["email"] = user[0]['email']
    dic["is superuser"] = user[0]['is_superuser']
    data.append(dic)

    return HttpResponse(data)

class SearchUserView(generics.ListCreateAPIView):
    '''
    search a user
    '''
    search_fields = ['first_name']
    filter_backends = (filters.SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SendMeetingRequest(APIView):
    '''
    send a meeting request
    '''
    def post(self,request):
        host_id = request.POST.get("host_id")
        user_id = request.POST.get("user_id")
        aval =  request.POST.get("availability")
        from_time = request.POST.get("from time")
        ft = datetime.strptime(from_time,'%Y-%m-%d %H:%M:%S').date()   
        to_time = request.POST.get("to time")
        et = datetime.strptime(to_time,'%Y-%m-%d %H:%M:%S').date()
        user = User.objects.filter(id=user_id).first()
        host = User.objects.filter(id=host_id).first()
        if ft==ft.today() and et == et.today() :
            MeetingRequest.objects.create(meeting_attender=user,meeting_host=host,from_time=from_time,to_time=to_time)
            return JsonResponse({"msg":"request for meeting is sent."})
        else:
            return JsonResponse({"msg":"Only today's date is allowed."})

class AllMeetingRequest(APIView):
    '''
    when a user logs in all meeting request appears.
    '''
    def get(self,request,id):
        user_id=User.objects.filter(id=id).first().id
        if MeetingRequest.objects.filter(meeting_host=user_id) or MeetingRequest.objects.filter(meeting_attender=user_id):
            all_request=MeetingRequest.objects.all()
            return JsonResponse({"all_requests":all_request})
        else:
            return JsonResponse({"msg":"No meetings"})

class MeetingResponseView(APIView):
    '''
    user respond to a meeting request notification when logs in.
    '''
    def post(self,request):
        user= request.POST.get("user")
        aval=request.POST.get("availability",None)
        request_id=request.POST.get("request_id")
        user = User.objects.filter(id=user).first()
        request_id=MeetingRequest.objects.filter(id=request_id).first()
        if aval == "YES":
            Availability.objects.create(user=user,meeting_request=request_id,availability=aval)
            return JsonResponse({"msg":"Meeting request is accepted."})
        else:
            Availability.objects.create(user=user,meeting_request=request_id,availability="NO")
            return JsonResponse({"msg":"Meeting request is rejected."})

class ArrangeMeeting(APIView):
    '''
    view to a arrange a meeting for an available user.
    '''

    def post(self,request):
        host_id=request.POST.get("host_id")
        attender_id = request.POST.get("attender_id")
        meeting_start_time = request.POST.get("meeting_time")
        ft = datetime.strptime(meeting_start_time,'%Y-%m-%d %H:%M:%S').date()   
        meeting_subject = request.POST.get("subject",None)
        host_id=User.objects.filter(id=host_id).first()
        attender_id=User.objects.filter(id=attender_id).first()
        if Availability.objects.filter(user=attender_id,availability="YES"):
            if ft==ft.today():
                if meeting_subject == None:
                    m=Meeting.objects.create(host=host_id,attender=attender_id,meeting_start_time=meeting_start_time,meeting_subject=None)
                    return JsonResponse({"msg":"meeting is scheduled."})
                else:
                    m=Meeting.objects.create(host=host_id,attender=attender_id,meeting_start_time=meeting_start_time,meeting_subject=meeting_start_time)
                    return JsonResponse({"msg":"meeting is scheduled."})
            else:
                return JsonResponse({"msg":"Enter today's date."})



