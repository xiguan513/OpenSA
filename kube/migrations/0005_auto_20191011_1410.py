# Generated by Django 2.1.5 on 2019-10-11 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0004_auto_20191011_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatepod',
            name='storage',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kube.TemplateStorage', verbose_name='存储'),
        ),
    ]
