# Generated by Django 2.1.5 on 2019-11-02 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0018_auto_20191102_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='updateinfo',
            old_name='build_gitid',
            new_name='build_uuid',
        ),
    ]
