# Generated by Django 2.1.5 on 2019-11-03 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0019_auto_20191102_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updateinfo',
            name='git_commit',
        ),
        migrations.RemoveField(
            model_name='updateinfo',
            name='update_tag',
        ),
        migrations.AlterField(
            model_name='deploystatus',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='release',
            name='create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='镜像创建时间'),
        ),
        migrations.AlterField(
            model_name='updateinfo',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='打包时间'),
        ),
        migrations.AlterField(
            model_name='updateinfo',
            name='image_env',
            field=models.CharField(max_length=10, null=True, verbose_name='项目环境'),
        ),
        migrations.AlterField(
            model_name='updateinfo',
            name='pro_env',
            field=models.CharField(max_length=10, null=True, verbose_name='运行环境'),
        ),
    ]
