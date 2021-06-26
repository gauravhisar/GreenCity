# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.functional import cached_property
from django.db.models import Manager,Sum,Count
from datetime import date
import logging


logger = logging.getLogger(__name__)
logger.info(__name__)

class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    contact_no = models.TextField(unique=True, null=True, blank=True)
    other_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + "(" + str(self.contact_no) + ")"

    class Meta:
        managed = True
        db_table = 'Dealer'

    @property
    def contact(self):
        if self.contact_no == None:
            return ""
        return self.contact_no

    @contact.setter
    def contact(self, contact):
        if contact == None or len(contact) == 0:
            self.contact_no = None
        self.contact_no = contact


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    contact_no = models.TextField(unique=True, null=True, blank=True)
    other_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + "(" + str(self.contact_no) + ")"

    class Meta:
        managed = True
        db_table = 'Customer'

    @property
    def contact(self):
        if self.contact_no == None:
            return ""
        return self.contact_no

    @contact.setter
    def contact(self, contact):
        if contact == None or len(contact) == 0:
            self.contact_no = None
        self.contact_no = contact

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_area = models.FloatField(blank=True, null=True)
    total_plots = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'Project'
   
    def __str__(self):
        return self.name

    @property
    def plots_sold(self):
        return self.plots.exclude(deal = None).aggregate(Count('id'))['id__count']

    @property
    def area_sold(self):
        areasold = self.plots.exclude(deal = None).aggregate(Sum('area'))['area__sum']
        return areasold if areasold != None else 0

class Plot(models.Model):
    id = models.AutoField(primary_key=True)
    plot_no = models.TextField(unique=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='plots')
    area = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.plot_no) + " ("+self.project.name + ")"

    class Meta:
        managed = True
        # abstract = True
        db_table = 'Plot'
        unique_together = ('plot_no', 'project')
    
    @property
    def amount(self):
        if (self.area != None and self.rate !=None):
            return self.area*self.rate
        return None

    @property
    def project_name(self):
        return self.project.name


class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    plot = models.OneToOneField(
        Plot, on_delete=models.DO_NOTHING, null=True, related_name='deal')
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, null=True, related_name='deals')
    dealer = models.ForeignKey(
        Dealer, null=True, on_delete=models.DO_NOTHING, related_name='deals')

    class Meta:
        managed = True
        db_table = 'Deal'

    def __str__(self):
        return self.plot.plot_no + " (" + self.plot.project.name + ")"

    @cached_property
    def get_aggregates(self):
        agg = self.payments.all().aggregate(total_amount_paid=Sum('net_amount_paid'),total_rebate=Sum('rebate'),total_interest_given=Sum('interest_given'))
        agg['total_amount_paid'] = agg.get('total_amount_paid') or 0
        agg['total_rebate'] = agg.get('total_rebate') or 0
        agg['total_interest_given'] = agg.get('total_interest_given') or 0
        # if not agg['total_amount_paid']:
        #     agg['total_amount_paid'] = 0
        # if not agg['total_rebate']:
        #     agg['total_rebate'] = 0
        # if not agg['total_interest_given']:
        #     agg['total_interest_given'] = 0

        agg['total_amount_covered'] = sum(agg.values())
        agg['balance'] = self.plot.amount - agg['total_amount_covered']
        agg = agg | self.dues.filter(due_date__gt = date.today()).aggregate(dues_upto_today = Sum('payable_amount'))
        if not agg['dues_upto_today']:
            agg['dues_upto_today'] = 0
        
        agg['penalty'] = agg['dues_upto_today'] > agg['total_amount_covered']
        return agg
        

class Due(models.Model):
    id = models.AutoField(primary_key=True)
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name='dues')
    due_date = models.DateField(blank=True, null=True)
    payable_amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.deal.plot.plot_no + " (" + self.deal.plot.project.name + ") -- " + str(self.id)

    class Meta:
        managed = True
        db_table = 'Dues'

    # @property
    # def paid(self):
    #     pass


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField(default=date.today, blank=True, null=True)
    interest_given = models.FloatField(blank=True, null=True)
    rebate = models.FloatField(blank=True, null=True)
    net_amount_paid = models.FloatField(
        null=True, blank=True)  # net amount paid by customer
    # amount = models.FloatField(blank=True, null=True)  = rebate + interest_given + net_amount_paid

    def __str__(self):
        return self.deal.plot.plot_no + " (" + self.deal.plot.project.name + ") -- " + self.id

    class Meta:
        managed = True
        db_table = 'Payment'


class CommissionPayment(models.Model):  # give
    id = models.AutoField(primary_key=True)
    deal = models.ForeignKey(
        Deal, on_delete=models.CASCADE, related_name='commission_payments')
    date = models.DateField(default=date.today, blank=True, null=True)
    amount = models.FloatField()

    def __str__(self):
        return self.dealer.name + self.id

    class Meta:
        managed = True
        db_table = 'CommissionPayment'
        verbose_name = "Commission Payment"
