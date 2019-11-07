# Generated by Django 2.1.5 on 2019-10-21 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0011_auto_20191021_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='镜像名字')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('branch_env', models.CharField(max_length=10, verbose_name='上线记录')),
                ('server_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kube.GitInfo', verbose_name='服务名称')),
            ],
            options={
                'verbose_name': '阿里云上线记录',
                'verbose_name_plural': '阿里云上线记录',
                'db_table': 'release',
                'ordering': ['-create_time'],
            },
        ),
    ]