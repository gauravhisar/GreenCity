# Generated by Django 3.2.4 on 2021-07-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0011_auto_20210702_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='plot_no',
            field=models.TextField(null=True),
        ),
    ]
