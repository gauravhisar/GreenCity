from rest_framework import serializers
from django.db.models import Sum
from datetime import date
import logging
from Home.models import Project, Plot, Customer, Dealer, Deal,Payment,Due,CommissionPayment


logger = logging.getLogger(__name__)
logger.info(__name__)


class ProjectSerializer(serializers.ModelSerializer):  # used by list view only
    class Meta:
        model = Project
        fields = ('id', 'name', 'address', 'total_plots', 'total_area','plots_sold','area_sold')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_no', 'other_info')


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'name', 'contact_no', 'other_info')


class DealSerializer(serializers.ModelSerializer): 
    "Serializer for both Detail and List Views  "
    plot_id = serializers.PrimaryKeyRelatedField(queryset = Plot.objects.all(),source = "plot")
    customer_id = serializers.PrimaryKeyRelatedField(queryset = Customer.objects.all(),write_only = True, source = "customer")
    dealer_id = serializers.PrimaryKeyRelatedField(queryset = Dealer.objects.all(),write_only = True, source = "dealer")
    customer = CustomerSerializer(read_only = True)
    dealer = DealerSerializer(read_only = True)
    
    class Meta:
        model = Deal
        fields = ('id','plot_id','customer_id','dealer_id','customer','balance','penalty','dealer')

    # def get_plot_id(self,data)
    def __str__(self):
        return 'Deal on PlotNo: ' + str(self.plot.plot_no) + 'of Project:' + str(self.plot.project.name)

class PlotSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only = True)
    class Meta:
        model = Plot
        fields = ('id', 'plot_no', 'project_id', 'project_name','area', 'rate', 'amount', 'deal')

    def create(self, validated_data):
        plot = Plot(
            id = validated_data.get('id'),
            project_id = self.context['view'].kwargs['project_id'],
            plot_no = validated_data.get('plot_no'),
            area = validated_data.get('area'),
            rate = validated_data.get('rate')
        )
        plot.save()
        return plot
        
        

class DueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Due
        fields = ('id','deal_id','due_date','payable_amount')


class PaymentSerializer(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = Payment
        fields = ('id','deal_id','date','interest_given','rebate','net_amount_paid')


class CommissionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionPayment
        fields = ('id','deal_id','date','amount')



class DealDetailSerializer(serializers.ModelSerializer):
    dealer = DealerSerializer(read_only = True)
    customer = CustomerSerializer(read_only = True)
    payments = PaymentSerializer(many = True,read_only = True)
    commission_payments = CommissionPaymentSerializer(many=True,read_only = True)
    dues = DueSerializer(many=True,read_only = True)

    class Meta:
        model = Deal
        fields = ('id', 'plot_id', 'customer', 'dues','payments','penalty','dealer', 'commission_payments',
                   'balance')
    
    def __str__(self):
        return 'Deal on PlotNo: ' + str(self.plot.plot_no) + 'of Project:' + str(self.plot.project.name)

# detail of plot with deal corresponding to it
class PlotDetailSerializer(serializers.ModelSerializer):
    deal = DealDetailSerializer(read_only=True)

    class Meta:
        model = Plot
        fields = ('id', 'plot_no', 'project_id', 'project_name','area', 'rate', 'amount','deal')


class ProjectDetailSerializer(serializers.ModelSerializer):
    plots = PlotSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'address',
                  'total_plots', 'total_area', 'plots_sold','area_sold','plots')


class CustomerDetailSerializer(serializers.ModelSerializer):
    deal = DealSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_no', 'other_info', 'deal')


class DealerDetailSerializer(serializers.ModelSerializer):
    deal = DealSerializer(many = True, read_only=True)
    
    class Meta:
        model = Dealer
        fields = ('id', 'name', 'contact_no', 'other_info', 'deal')


class DealsFileUploadSerializer(serializers.Serializer):
    id = serializers.ModelField(Project)
    file = serializers.FileField()

    class Meta:
        fields = ['id', 'file']
