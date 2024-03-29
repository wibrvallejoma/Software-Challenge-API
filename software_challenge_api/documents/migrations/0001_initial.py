# Generated by Django 3.1.13 on 2021-08-22 00:32

from django.db import migrations, models
import software_challenge_api.documents.models.documents


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=software_challenge_api.documents.models.documents.get_upload_path)),
                ('file_type', models.CharField(choices=[('file', 'File'), ('folder', 'Folder')], max_length=10)),
                ('state', models.CharField(choices=[('active', 'active'), ('obsolete', 'obsolete')], default='active', max_length=10)),
                ('childs', models.ManyToManyField(blank=True, null=True, related_name='parent', to='documents.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
