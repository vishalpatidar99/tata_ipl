
from ipl.views import *
from django.urls import path


urlpatterns = [
    
    path('',user_list),
    path('<int:id>',user_details,name='user_details'),
    path('schedule/',schedule,name='scheduel'),
    path('search_user/', SearchUserView.as_view()),
    path('send_meeting_request/',SendMeetingRequest.as_view()),
    path('all_meetings/<int:id>',AllMeetingRequest.as_view()),
    path("meeting_response/",MeetingResponseView.as_view()),
    path("arrange_meeting/",ArrangeMeeting.as_view()),
]
