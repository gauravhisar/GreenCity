from rest_framework import serializers
from django.db.models import Sum
from django.utils.functional import cached_property
from datetime import date
import logging

from rest_framework.fields import DictField
from Home.models import Project, Plot, Customer, Dealer, Deal,Payment,Due,CommissionPayment


# logger = logging.getLogger(__name__)
# logger.info(__name__)


class ProjectSerializer(serializers.ModelSerializer):  # used by list view only
    class Meta:
        model = Project
        fields = ('id', 'name', 'address', 'total_plots', 'total_area','plots_sold','area_sold','plots_left','area_left')


class CustomerSerializer(serializers.ModelSerializer):
    contact_no = serializers.CharField(max_length=10, source = "contact", required = False, allow_null = True, allow_blank = True)
    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_no', 'other_info')


class DealerSerializer(serializers.ModelSerializer):
    contact_no = serializers.CharField(max_length=10, source = "contact",required = False, allow_null = True, allow_blank = True)
    class Meta:
        model = Dealer
        fields = ('id', 'name', 'contact_no', 'other_info')

    def to_representation(self, instance):
        # req = self.context['request']
        # print(req.user, req.auth)
        return super().to_representation(instance)

class DueSerializer(serializers.ModelSerializer):
    paid = serializers.FloatField(read_only = True)
    due_date = serializers.DateField(input_formats = ["%d-%m-%Y", 'iso-8601'])
    class Meta:
        model = Due
        fields = ('id','deal_id','due_date','payable_amount', 'paid')
    
    def create(self, validated_data): # now there is no need for client to pass project_id in the request
        due = Due(
            deal_id = self.context['view'].kwargs.get('deal_id'),
            due_date = validated_data.get('due_date'),
            payable_amount = validated_data.get('payable_amount')
        )
        due.save()
        return due

class PaymentSerializer(serializers.ModelSerializer):
    ''''''
    class Meta:
        model = Payment
        fields = ('id','deal_id','date','interest_given','rebate','net_amount_paid')

    def create(self, validated_data): # now there is no need for client to pass project_id in the request
        payment = Payment(
            deal_id = self.context['view'].kwargs.get('deal_id'),
            date = validated_data.get('date'),
            interest_given = validated_data.get('interest_given'),
            rebate = validated_data.get('rebate'),
            net_amount_paid = validated_data.get('net_amount_paid')
        )
        payment.save()
        return payment


class CommissionPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionPayment
        fields = ('id','deal_id','date','amount')

    def create(self, validated_data): # now there is no need for client to pass project_id in the request
        cp = CommissionPayment(
            deal_id = self.context['view'].kwargs.get('deal_id'),
            date = validated_data.get('date'),
            amount = validated_data.get('amount')
        )
        cp.save()
        return cp


class DealSerializer(serializers.ModelSerializer): 
    "Serializer for both Detail and List Views  "

    #both read and write fields
    plot_id = serializers.PrimaryKeyRelatedField(queryset = Plot.objects.all(),source = "plot")

    # write_only fields
    customer_id = serializers.PrimaryKeyRelatedField(queryset = Customer.objects.all(),write_only = True, source = "customer")
    dealer_id = serializers.PrimaryKeyRelatedField(queryset = Dealer.objects.all(),write_only = True, source = "dealer")
    
    # read_only fields
    customer = CustomerSerializer(read_only = True)
    dealer = DealerSerializer(read_only = True)
    dues = DueSerializer(many = True, read_only = True, allow_empty = True) 
    unpaid_dues_in_upcoming_30_days = serializers.BooleanField(read_only=True)

    balance = serializers.FloatField(read_only = True)
    penalty = serializers.BooleanField(read_only = True)
    total_rebate = serializers.FloatField(read_only = True)
    total_interest_given = serializers.FloatField(read_only = True)
    total_amount_paid = serializers.FloatField(read_only = True)
    # next_due = DueSerializer(read_only = True)
    # unpaid_dues_in_upcoming_30_days = serializers.BooleanField(read_only=True)
    unpaid_dues = DueSerializer(many=True, read_only=True)
    total_commission_paid = serializers.FloatField(read_only = True)

    class Meta:
        model = Deal
        exclude = ['plot']

    def to_representation(self, instance):
        agg = instance.get_aggregates
        instance.balance = agg['balance']
        instance.penalty = agg['penalty']
        instance.total_rebate = agg['total_rebate']
        instance.total_interest_given = agg['total_interest_given']
        instance.total_amount_paid = agg['total_amount_paid']
        # instance.next_due = agg['next_due']
        # instance.unpaid_dues_in_upcoming_30_days = agg['unpaid_dues_in_upcoming_30_days']
        instance.unpaid_dues = agg['unpaid_dues']
        instance.total_commission_paid = agg['total_commission_paid']
        data = super().to_representation(instance)
        for i in range(len(agg['dues'])):
            data['dues'][i]['paid'] = agg['dues'][i].paid
        # if not data['next_due']['id']:
        #     data['next_due'] = None
        # data['next_due']['paid'] = agg['next_due'].paid
        return data
        

    # def get_plot_id(self,data)
    def __str__(self):
        return 'Deal on PlotNo: ' + str(self.plot.plot_no) + 'of Project:' + str(self.plot.project.name)

class PlotSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only = True)
    plc = serializers.FloatField(default = 0, required = False)
    class Meta:
        model = Plot
        fields = ('id', 'plot_no', 'project_id', 'project_name','area', 'rate','plc','amount', 'deal')

    def create(self, validated_data): # now there is no need for client to pass project_id in the request
        plot = Plot(
            # id = validated_data.get('id'),
            project_id = self.context['view'].kwargs['project_id'],
            plot_no = validated_data.get('plot_no'),
            area = validated_data.get('area'),
            rate = validated_data.get('rate'),
            plc = validated_data.get('plc')
        )
        plot.save()
        return plot



class DealDetailSerializer(DealSerializer):
    payments = PaymentSerializer(many = True,read_only = True, allow_empty = True)
    commission_payments = CommissionPaymentSerializer(many=True,read_only = True, allow_empty = True)
    # dues = DueSerializer(many=True,read_only = True)
    unpaid_dues_in_upcoming_30_days = serializers.BooleanField(read_only=True)


    class Meta:
        model = Deal
        exclude = ['plot']
    
    def __str__(self):
        return 'Deal on PlotNo: ' + str(self.plot.plot_no) + 'of Project:' + str(self.plot.project.name)

# detail of plot with deal corresponding to it
class PlotDetailSerializer(serializers.ModelSerializer):
    deal = DealDetailSerializer(read_only=True)
    plc = serializers.FloatField(default = 0,required = False)

    class Meta:
        model = Plot
        fields = ('id', 'plot_no', 'project_id', 'project_name','area', 'rate','plc', 'amount','deal')


class ProjectDetailSerializer(serializers.ModelSerializer):
    plots = PlotSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'address',
                  'total_plots', 'total_area', 'plots_sold','area_sold', 'plots_left', 'area_left','plots')

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        mapped_plots = {}
        for plot in data['plots']:
            mapped_plots[plot['id']] = plot
        data['plots'] = mapped_plots
        return data


class CustomerDetailSerializer(CustomerSerializer):
    deal = DealSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_no', 'other_info', 'deal')


class DealerDetailSerializer(DealerSerializer):
    deal = DealSerializer(many = True, read_only=True)
    
    class Meta:
        model = Dealer
        fields = ('id', 'name', 'contact_no', 'other_info', 'deal')


class DealsFileUploadSerializer(serializers.Serializer):
    id = serializers.ModelField(Project)
    file = serializers.FileField()

    class Meta:
        fields = ['id', 'file']

