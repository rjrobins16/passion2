# Generated by Django 2.0.6 on 2020-01-06 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PrimpApp', '0002_auto_20200105_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alluser',
            name='is_stylist',
        ),
    ]