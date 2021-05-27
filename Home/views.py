from django.shortcuts import render
from django.http import HttpResponse
from Home.models import Project
# Create your views here.


# to get all the projects 
def get_projects(*args,**kwargs):
    data = []
    for i in Project.objects.all():
        data.append(i)
    return HttpResponse(data[0].name)