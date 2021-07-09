# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.functional import cached_property
from django.db.models import Sum,Count
from datetime import date, timedelta 
# import logging
# ['']

# logger = logging.getLogger(__name__)
# logger.info(__name__)

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
            # print(contact)
            self.contact_no = None
        else: 
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
    @property
    def plots_left(self):
        return self.total_plots - self.plots_sold
    @property
    def area_left(self):
        return self.total_area - self.area_sold

class Plot(models.Model):
    id = models.AutoField(primary_key=True)
    plot_no = models.TextField(unique=True, null=True)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='plots')
    area = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    plc = models.DecimalField(blank=True, default= 0, decimal_places=2, max_digits = 10)

    def __str__(self):
        return str(self.plot_no) + " ("+self.project.name + ")"

    class Meta:
        managed = True
        db_table = 'Plot'
        unique_together = ('plot_no', 'project')
    
    @property
    def amount(self):
        if (self.area != None and self.rate !=None and self.plc != None):
            return int(self.area*self.rate*float(1 + self.plc/100))
        return None

    @property
    def project_name(self):
        return self.project.name


class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    plot = models.OneToOneField(
        Plot, on_delete=models.CASCADE, null=True, related_name='deal')
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
        agg = agg | self.commission_payments.all().aggregate(total_commission_paid = Sum('amount'))
        for key in agg:
            if agg[key] == None:
                agg[key] = 0
        total_amount_covered = agg['total_amount_covered'] = agg['total_amount_paid'] + agg['total_rebate'] + agg['total_interest_given']


        dues = self.dues.all()

        # dues_paid = []
        unpaid_dues = []
        agg['next_due'] = Due()
        unpaid_dues_in_upcoming_30_days = []
        penalty = False            # penalty is True if a due date is crossed and still havent received the payment

        tday = date.today()
        sum_of_payable_amount = 0

        i = 0
        while i <  len(dues):
            due = dues[i]
            sum_of_payable_amount += due.payable_amount
            if total_amount_covered >= sum_of_payable_amount:
                due.paid = due.payable_amount
                # dues_paid.append(due)
            else:
                due.paid = due.payable_amount - (sum_of_payable_amount - total_amount_covered)
                unpaid_dues.append(due)
                agg['next_due'] = due
                if due.due_date < tday:
                    unpaid_dues_in_upcoming_30_days.append(due) 
                    penalty = True
                break
            i+=1

        for j in range(i+1,len(dues)): # left all the dues are unpaid
            due = dues[j]
            due.paid = 0
            unpaid_dues.append(due)
            if due.due_date < tday + timedelta(days = 30):
                unpaid_dues_in_upcoming_30_days.append(due)

        # agg['this_month_dues'] = self.dues.filter(due_date__gte = date.today()).filter(due_date__lte = date.today() + timedelta(days=30)).order_by('due_date')
        agg['dues'] = dues
        agg['unpaid_dues_in_upcoming_30_days'] = len(unpaid_dues_in_upcoming_30_days)
        agg['unpaid_dues'] = unpaid_dues
        agg['balance'] = self.plot.amount - total_amount_covered
        agg['penalty'] = penalty
        return agg
        
    # @cached_property
    # def total_amount_covered(self):
    #     agg = self.payments.all().aggregate(total_amount_paid=Sum('net_amount_paid'),total_rebate=Sum('rebate'),total_interest_given=Sum('interest_given'))
    #     total_amount_covered = 0
    #     for key in agg:
    #         if agg[key] == None:
    #             agg[key] = 0
    #         total_amount_covered += agg[key]
    #     return total_amount_covered
        


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
        ordering = ['due_date']



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
        return str(self.deal.plot.plot_no) + " (" + self.deal.plot.project.name + ") -- " + str(self.id)

    class Meta:
        managed = True
        db_table = 'Payment'
        ordering = ['date']


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
        ordering = ['date']
