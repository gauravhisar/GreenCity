# from django.core.files.base import File
# from django.db.models import query
# from django.http import HttpResponse
import logging
from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from Home import serializers
from Home.models import Project, Customer, Dealer, Plot, Deal,Payment,Due,CommissionPayment
# from Home.serializers import CustomerSerializer, DealerSerializer, PlotSerializer, DealSerializer, DealsFileUploadSerializer
# Create your views here.


# Get an instance of a logger
# logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'retrieve': serializers.ProjectDetailSerializer,
        'list': serializers.ProjectSerializer,
        'create': serializers.ProjectSerializer,
        'destroy': serializers.ProjectSerializer,
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
        'destroy': serializers.PlotSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.PlotSerializer)

    def get_queryset(self):
        return Plot.objects.filter(project_id = self.kwargs['project_id'])


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_classes = {
        'retrieve': serializers.CustomerDetailSerializer,
        'list': serializers.CustomerSerializer,
        'create': serializers.CustomerSerializer,
        'destroy': serializers.CustomerSerializer,
        'update': serializers.CustomerSerializer,
        'partial_update': serializers.CustomerSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.CustomerSerializer)


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_classes = {
        'retrieve': serializers.DealerDetailSerializer,
        'list': serializers.DealerSerializer,
        'create': serializers.DealerSerializer,
        'destroy': serializers.DealerSerializer,
        'update': serializers.DealerSerializer,
        'partial_update': serializers.DealerSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.DealerSerializer)


class DealViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        'retrieve': serializers.DealDetailSerializer,
        'create': serializers.DealDetailSerializer,
        'list': serializers.DealSerializer,
        'destroy': serializers.DealSerializer,
        'update': serializers.DealSerializer,
        'partial_update': serializers.DealSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.DealSerializer)

    def get_queryset(self):
        return Deal.objects.filter(plot__project_id = self.kwargs['project_id'])

class DueViewSet(viewsets.ModelViewSet):
    # serializer_class = serializers.DueSerializer
    serializer_classes = {
        'retrieve': serializers.DueSerializer,
        'list': serializers.DueSerializer,
        'destroy': serializers.DueDetailSerializer,
        'create': serializers.DueDetailSerializer,
        'update': serializers.DueDetailSerializer,
        'partial_update': serializers.DueDetailSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.DueSerializer)

    def get_queryset(self):
        return Due.objects.filter(deal_id = self.kwargs['deal_id'])

    def destroy(self, request, *args, **kwargs):
        dues = list(self.get_queryset()) # dues is orderec by date
        last_due = dues.pop()
        instance = self.get_object()
        if last_due.id == instance.id:
            return Response(data = "You cannot delete last Due", status = status.HTTP_400_BAD_REQUEST)
        instance.delete()

        percentage_sum = sum([float(dues[i].payable_amount_percentage) for i in range(len(dues))]) - float(instance.payable_amount_percentage)
        if percentage_sum > 100:
            return Response(data = "Dues Percentage Cannot be greater than 100", status = status.HTTP_400_BAD_REQUEST)
        last_due.payable_amount_percentage = 100 - percentage_sum
        if len(dues) > 1:
            last_due.due_date = dues[-1].due_date if dues[-1].due_date != instance.due_date else dues[-2].due_date
        last_due.save()
        
        serializer = serializers.DealSerializer(Deal.objects.get(id=kwargs['deal_id']))
        return Response(data = {'deal':serializer.data}, status=status.HTTP_200_OK)



class PaymentViewSet(viewsets.ModelViewSet):
    # serializer_class = serializers.PaymentSerializer
    serializer_classes = {
        'retrieve': serializers.PaymentSerializer,
        'list': serializers.PaymentSerializer,
        'destroy': serializers.PaymentDetailSerializer,
        'create': serializers.PaymentDetailSerializer,
        'update': serializers.PaymentDetailSerializer,
        'partial_update': serializers.PaymentDetailSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.PaymentSerializer)

    def get_queryset(self):
        return Payment.objects.filter(deal_id = self.kwargs['deal_id'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        serializer = serializers.DealSerializer(Deal.objects.get(id=kwargs['deal_id']))
        return Response(data = {'deal':serializer.data}, status=status.HTTP_200_OK)
        # return super().destroy(request, *args, **kwargs)


class CommissionPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommissionPaymentSerializer
    serializer_classes = {
        'retrieve': serializers.CommissionPaymentSerializer,
        'list': serializers.CommissionPaymentSerializer,
        'destroy': serializers.CommissionPaymentDetailSerializer,
        'create': serializers.CommissionPaymentDetailSerializer,
        'update': serializers.CommissionPaymentDetailSerializer,
        'partial_update': serializers.CommissionPaymentDetailSerializer,
    }
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, serializers.CommissionPaymentSerializer)

    def get_queryset(self):
        return CommissionPayment.objects.filter(deal_id = self.kwargs['deal_id'])

    # return whole deal data after deletion of Commission
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        serializer = serializers.DealSerializer(Deal.objects.get(id=kwargs['deal_id']))
        return Response(data = {'deal':serializer.data}, status=status.HTTP_200_OK)

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
        print("I got the file!")
        return Response(r)
