# Generated by Django 2.1.5 on 2019-11-07 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0030_auto_20191107_1514'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='release',
            unique_together={('server_name', 'branch_env')},
        ),
    ]