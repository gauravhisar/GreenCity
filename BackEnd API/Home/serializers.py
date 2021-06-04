from rest_framework import serializers
from Home.models import Project, Plot, Customer, Dealer, Deal
import logging


logger = logging.getLogger(__name__)


class ProjectSerializer(serializers.ModelSerializer):  # used by list view only
    class Meta:
        model = Project
        fields = ('id', 'name', 'address', 'total_area', 'total_plots')


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ('id', 'plot', 'customer', 'rebate', 'dealer', 'commission')

    def __str__(self):
        return 'Deal on PlotNo: ' + str(self.plot.plot_no) + 'of Project:' + str(self.plot.project.name)


# listing all the plots without listing deal corresponding to it
class PlotSerializer(serializers.ModelSerializer):
    # will be used only when creating new plots
    class Meta:
        model = Plot
        fields = ('id', 'plot_no', 'project', 'area', 'rate')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'contact_no', 'other_info')


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id', 'name', 'contact_no', 'other_info')


class DealDetailSerializer(serializers.ModelSerializer):
    # used in PlotDetailSerializer below
    # will also be used to update, delete and retrieve
    customer = CustomerSerializer(read_only=True)
    dealer = DealerSerializer(read_only=True)
    balance = serializers.SerializerMethodField('get_balance')

    class Meta:
        model = Deal
        fields = ('id', 'plot', 'customer', 'rebate',
                  'dealer', 'commission', 'balance')

    def get_balance(self, instance):
        return 100  # NEED TO CHANGE

    def __str__(self):
        return 'Deal on PlotNo: ' + str(self.plot.plot_no) + 'of Project:' + str(self.plot.project.name)


# detail of plot with deal corresponding to it
class PlotDetailSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField('get_amount')
    # here, if the variable name is another than deal, we can add source = deal(related_name) otherwise it will consider source  = variablename only
    deal = DealDetailSerializer(read_only=True)

    class Meta:
        model = Plot
        fields = ('id', 'plot_no', 'project', 'area', 'rate', 'deal', 'amount')

    def get_amount(self, id,**kwargs):
        logger.info("Amount Calculated for plot : " + id.plot_no )
        return id.rate * id.area


# used by detail view only
class ProjectDetailSerializer(serializers.ModelSerializer):
    # plots with all their deals
    plots = PlotDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'address',
                  'total_area', 'total_plots', 'plots')


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
