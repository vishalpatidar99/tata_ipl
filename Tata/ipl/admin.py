from pickle import ADDITEMS
from django.contrib import admin
from .models import *
admin.site.register(MeetingRequest)
admin.site.register(Availability)
admin.site.register(Meeting)
admin.site.register(MeetingHistory)
# Register your models here.
