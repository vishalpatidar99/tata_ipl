from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class MeetingRequest(models.Model):
    meeting_host = models.ForeignKey(User,on_delete = models.CASCADE, related_name="meeting_host")
    meeting_attender = models.ForeignKey(User,on_delete = models.CASCADE, related_name="meeting_attender")
    from_time = models.DateTimeField(auto_now_add=False)
    to_time = models.DateTimeField(auto_now_add=False)

class Availability(models.Model):
    AVAL = [
    ('YES', 'YES'),
    ('NO', 'NO'),
    ]
    user = models.ForeignKey(User,on_delete = models.CASCADE, related_name="user")
    meeting_request = models.ForeignKey(MeetingRequest,on_delete = models.CASCADE, related_name="meeting_request")
    availability = models.CharField(max_length=10,choices=AVAL)
    # from_time1 = models.DateTimeField(auto_now_add=False)
    # to_time1 = models.DateTimeField(auto_now_add=False)

class Meeting(models.Model):
    host = models.ForeignKey(User,on_delete = models.CASCADE, related_name="host")
    attender = models.ForeignKey(User,on_delete = models.CASCADE,related_name="attender")
    meeting_start_time = models.DateTimeField(auto_now_add=False)
    meeting_subject = models.CharField(max_length=50,null=True,blank=True)
    # end_time = models.DateTimeField(auto_now_add=False)

class MeetingHistory(models.Model):
    meeting = models.ForeignKey(Meeting,on_delete = models.CASCADE, related_name="meeting")
    end_time = models.DateTimeField(auto_now_add=True)
    total_duration = models.IntegerField()
    ratings = models.IntegerField()

    def total_duration(self):
        diff = Meeting.start_time - MeetingHistory.end_time
        return diff


# Create your models here.
