# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Client(models.Model):
    id = models.AutoField()
    name = models.TextField()
    contact_no = models.TextField(unique=True, blank=True, null=True)
    other_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Client'


class ClientRelation(models.Model):
    id = models.AutoField(blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    relation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Client_Relation'


class Deal(models.Model):
    id = models.AutoField(blank=True, null=True)
    plot_id = models.IntegerField(blank=True, null=True)
    cust_id = models.IntegerField(blank=True, null=True)
    rebate = models.IntegerField(blank=True, null=True)
    dealer_id = models.IntegerField(blank=True, null=True)
    commission = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Deal'


class Dues(models.Model):
    id = models.AutoField()
    deal_id = models.IntegerField()
    due_date = models.TextField(blank=True, null=True)
    payable_amount = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Dues'


class Payment(models.Model):
    id = models.AutoField()
    deal_id = models.IntegerField()
    date = models.TextField(blank=True, null=True)
    amount_paid = models.FloatField(blank=True, null=True)
    interest = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Payment'


class Plot(models.Model):
    id = models.AutoField()
    plot_no = models.TextField()
    project_id = models.IntegerField()
    area = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Plot'


class Project(models.Model):
    id = models.AutoField()
    name = models.TextField()
    address = models.TextField(blank=True, null=True)
    total_area = models.FloatField(blank=True, null=True)
    total_plots = models.IntegerField(db_column='total_pLots', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Project'
