# Generated by Django 3.1.13 on 2021-08-22 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20210822_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='file_type',
            field=models.CharField(choices=[('file', 'File'), ('folder', 'Folder')], default='file', max_length=25),
        ),
        migrations.AlterField(
            model_name='document',
            name='state',
            field=models.CharField(choices=[('active', 'active'), ('obsolete', 'obsolete')], default='active', max_length=25),
        ),
    ]
