# Generated by Django 2.1.5 on 2019-10-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0016_auto_20191023_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='branch_env',
            field=models.CharField(max_length=50, verbose_name='上线分支'),
        ),
    ]
