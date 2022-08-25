
from ipl.views import *
from django.urls import path


urlpatterns = [
    
    path('',user_list),
    path('<int:id>',user_details,name='user_details'),
    path('schedule/',schedule,name='scheduel'),


   

]
