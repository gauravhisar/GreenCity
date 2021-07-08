# from django.core.files.base import File
# from django.db.models import query
# from django.http import HttpResponse
import logging
from rest_framework import viewsets,permissions
from rest_framework.response import Response
from Home import serializers
from Home.models import Project, Customer, Dealer, Plot, Deal,Payment,Due,CommissionPayment
# from Home.serializers import CustomerSerializer, DealerSerializer, PlotSerializer, DealSerializer, DealsFileUploadSerializer
# Create your views here.


# Get an instance of a logger
# logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'retrieve': serializers.ProjectDetailSerializer,
        'list': serializers.ProjectSerializer,
        'create': serializers.ProjectSerializer,
        'delete': serializers.ProjectSerializer,
        'update': serializers.ProjectSerializer,
        'partial_update': serializers.ProjectSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.ProjectSerializer)


class PlotViewSet(viewsets.ModelViewSet):
    # queryset = Plot.objects.all()  # this queryset will be seen in the view
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_classes = {
        'retrieve': serializers.PlotDetailSerializer,
        'update': serializers.PlotDetailSerializer,
        'partial_update': serializers.PlotDetailSerializer,
        'list': serializers.PlotSerializer,
        'create': serializers.PlotSerializer,
        'delete': serializers.PlotSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.PlotSerializer)

    def get_queryset(self):
        return Plot.objects.filter(project_id = self.kwargs['project_id'])


class CustomerViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Customer.objects.all()
    serializer_classes = {
        'retrieve': serializers.CustomerDetailSerializer,
        'list': serializers.CustomerSerializer,
        'create': serializers.CustomerSerializer,
        'delete': serializers.CustomerSerializer,
        'update': serializers.CustomerSerializer,
        'partial_update': serializers.CustomerSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.CustomerSerializer)


class DealerViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Dealer.objects.all()
    serializer_classes = {
        'retrieve': serializers.DealerDetailSerializer,
        'list': serializers.DealerSerializer,
        'create': serializers.DealerSerializer,
        'delete': serializers.DealerSerializer,
        'update': serializers.DealerSerializer,
        'partial_update': serializers.DealerSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.DealerSerializer)


class DealViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_classes = {
        'retrieve': serializers.DealDetailSerializer,
        'list': serializers.DealSerializer,
        'create': serializers.DealSerializer,
        'delete': serializers.DealSerializer,
        'update': serializers.DealSerializer,
        'partial_update': serializers.DealSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.DealSerializer)

    def get_queryset(self):
        return Deal.objects.filter(plot__project_id = self.kwargs['project_id'])

class DueViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.DueSerializer

    def get_queryset(self):
        return Due.objects.filter(deal_id = self.kwargs['deal_id'])



class PaymentViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(deal_id = self.kwargs['deal_id'])


class CommissionPaymentViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.CommissionPaymentSerializer

    def get_queryset(self):
        return CommissionPayment.objects.filter(deal_id = self.kwargs['deal_id'])


class DealsFileUploadViewSet(viewsets.ViewSet):
    # parser_classes = [parsers.FileUploadParser]
    serializer_class = serializers.DealsFileUploadSerializer

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
