# Generated by Django 2.1.5 on 2019-10-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0012_release'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='server_name',
            field=models.CharField(max_length=100, verbose_name='服务名称'),
        ),
    ]
