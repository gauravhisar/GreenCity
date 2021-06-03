from rest_framework import serializers
from Home.models import Project, Plot, Customer, Dealer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','name','address','total_area','total_plots')


class PlotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plot
        fields = ('id','plot_no','project','area','rate')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id','name','contact_no','other_info')


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('id','name','contact_no','other_info')



class DealsFileUploadSerializer(serializers.Serializer):
    id = serializers.ModelField(Project)
    file = serializers.FileField()
    class Meta:
        fields = ['id','file']

