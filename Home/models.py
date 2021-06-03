# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    contact_no = models.TextField(unique=True,null=True)
    other_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + "(" + self.contact_no + ")"

    class Meta:
        managed = True
        db_table = 'Dealer'
        

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    contact_no = models.TextField(unique=True,null = True)
    other_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name) + "(" + self.contact_no + ")"

    class Meta:
        managed = True
        db_table = 'Customer'


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True, null=True)
    address = models.TextField(blank=True, null=True)
    total_area = models.FloatField(blank=True, null=True)
    total_plots = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'Project'


class Plot(models.Model):
    id = models.AutoField(primary_key=True)
    plot_no = models.TextField(unique=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='plots')
    area = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.plot_no + " ("+self.project.name + ")"

    # def plots_of_given_project_id(self,project_id):  # remember this
    #     return Project.objects.get(id = project_id).plots.all()

    class Meta:
        managed = True
        db_table = 'Plot'


class Deal(models.Model):
    id = models.AutoField(primary_key=True)
    plot = models.OneToOneField(Plot,on_delete = models.DO_NOTHING,null = True )
    customer = models.ForeignKey(Customer,on_delete = models.DO_NOTHING,null = True)
    rebate = models.FloatField(blank=True, null=True)
    dealer = models.ForeignKey(Dealer,null=True,on_delete = models.DO_NOTHING)
    commission = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.plot.plot_no + " (" + self.plot.project.name + ")"
    class Meta:
        managed = True
        db_table = 'Deal'


class Due(models.Model):
    id = models.AutoField(primary_key=True)
    deal = models.ForeignKey(Deal,on_delete= models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    payable_amount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.deal.plot.plot_no + " (" + self.deal.plot.project.name + ") -- " +  self.id

    class Meta:
        managed = True
        db_table = 'Dues'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    deal = models.ForeignKey(Deal,on_delete= models.CASCADE)
    date = models.DateField(blank=True, null=True)
    amount_paid = models.FloatField(blank=True, null=True)
    interest = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.deal.plot.plot_no + " (" + self.deal.plot.project.name + ") -- " +  self.id
        
    class Meta:
        managed = True
        db_table = 'Payment'