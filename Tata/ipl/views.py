from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
def user_list(request):
    return render(request,'user_list.html',{'users':User.objects.all()})

def user_details(request,id):
    return render(request,'user_details.html',{'user ':User.objects.filter(id=id).first()})
