# Generated by Django 3.1.13 on 2021-08-22 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20210822_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='childs',
        ),
        migrations.AlterField(
            model_name='document',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='documents.document'),
        ),
    ]
