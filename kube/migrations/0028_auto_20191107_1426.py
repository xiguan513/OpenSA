# Generated by Django 2.1.5 on 2019-11-07 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0027_auto_20191106_1500'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='release',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='release',
            name='build_uuid',
        ),
    ]
