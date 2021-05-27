from django.urls import path,include
from Home.views import get_projects

urlpatterns = [
    path('projects/', get_projects,name = "projects"),
]