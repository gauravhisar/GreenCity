from django.core.files.base import File
from django.http import HttpResponse
import logging

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from Home import serializers
from Home.models import Project, Customer, Dealer, Plot, Deal
from Home.serializers import CustomerSerializer, DealerSerializer, PlotSerializer, DealSerializer, DealsFileUploadSerializer
# Create your views here.


# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'list': serializers.ProjectSerializer,
        'create': serializers.ProjectSerializer,
        'retrieve': serializers.ProjectDetailSerializer,
        'delete': serializers.ProjectDetailSerializer,
        'update': serializers.ProjectDetailSerializer,
        'partial_update': serializers.ProjectDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.ProjectSerializer)


class PlotViewSet(viewsets.ModelViewSet):
    queryset = Plot.objects.all()  # this queryset will be seen in the view
    serializer_class = PlotSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_classes = {
        'list': serializers.CustomerSerializer,
        'create': serializers.CustomerSerializer,
        'retrieve': serializers.CustomerDetailSerializer,
        'delete': serializers.CustomerDetailSerializer,
        'update': serializers.CustomerDetailSerializer,
        'partial_update': serializers.CustomerDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.CustomerSerializer)


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_classes = {
        'list': serializers.DealerSerializer,
        'create': serializers.DealerSerializer,
        'retrieve': serializers.DealerDetailSerializer,
        'delete': serializers.DealerDetailSerializer,
        'update': serializers.DealerDetailSerializer,
        'partial_update': serializers.DealerDetailSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.DealerSerializer)


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class DealsFileUploadViewSet(viewsets.ViewSet):
    # parser_classes = [parsers.FileUploadParser]
    serializer_class = DealsFileUploadSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        file_obj = request.FILES.get('file')
        content_type = file_obj.content_type
        print(dir(file_obj))
        with open("new.pdf", "wb") as s:
            s.write(file_obj.read())
            s.close()

        r = "POST API and you have uploaded a {} file".format(content_type)
        print("I got the file bitch")
        return Response(r)
