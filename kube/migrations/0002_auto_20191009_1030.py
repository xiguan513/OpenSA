# Generated by Django 2.1.5 on 2019-10-09 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatepod',
            name='periodSeconds',
            field=models.CharField(max_length=10, verbose_name='测试间隔'),
        ),
    ]
