# Generated by Django 3.1.13 on 2021-08-22 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='document',
            name='name',
        ),
    ]