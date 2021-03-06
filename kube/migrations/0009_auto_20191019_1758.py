# Generated by Django 2.1.5 on 2019-10-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0008_auto_20191012_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deploystatus',
            name='status',
        ),
        migrations.AddField(
            model_name='deploystatus',
            name='env_name',
            field=models.CharField(max_length=50, null=True, verbose_name='环境更新'),
        ),
        migrations.AddField(
            model_name='deploystatus',
            name='renew_status',
            field=models.CharField(max_length=50, null=True, verbose_name='更新状态'),
        ),
        migrations.AddField(
            model_name='deploystatus',
            name='uuid',
            field=models.UUIDField(null=True, verbose_name='uuid'),
        ),
        migrations.AlterField(
            model_name='deploystatus',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='打包时间'),
        ),
        migrations.AlterField(
            model_name='deploystatus',
            name='server_name',
            field=models.CharField(max_length=250, null=True, verbose_name='服务名称'),
        ),
    ]
