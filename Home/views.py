from django.core.files.base import File
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
# from rest_framework.decorators import parser_classes
from Home.models import  Project, Customer, Dealer, Plot
from Home.serializers import  ProjectSerializer, CustomerSerializer, DealerSerializer, PlotSerializer,DealsFileUploadSerializer
from rest_framework import generics,viewsets
# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


# class PlotViewSet(viewsets.ModelViewSet):
#     queryset = Plot.objects.all()  # this queryset will be seen in the view
#     serializer_class = PlotSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

class DealsFileUploadViewSet(viewsets.ViewSet):
    # parser_classes = [parsers.FileUploadParser]
    serializer_class = DealsFileUploadSerializer

    def list(self, request):
        return response.Response("GET API")

    def create(self,request):
        file_obj = request.FILES.get('file')
        content_type = file_obj.content_type
        print(dir(file_obj))
        with open("new.pdf","wb") as s:
            s.write(file_obj.read())
            s.close()

        
        r = "POST API and you have uploaded a {} file".format(content_type)
        print("I got the file bitch")
        return response.Response(r)
