# Generated by Django 2.1.5 on 2019-10-11 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kube', '0003_auto_20191009_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stroname', models.CharField(max_length=100, verbose_name='存储名称')),
                ('claimname', models.CharField(max_length=100, verbose_name='pvc名称')),
                ('mountpath', models.CharField(max_length=100, verbose_name='挂载路径')),
            ],
            options={
                'verbose_name': '存储模板',
                'verbose_name_plural': '存储模板',
                'db_table': 'storage',
            },
        ),
        migrations.AddField(
            model_name='templatepod',
            name='storage',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='kube.TemplateStorage', verbose_name='存储'),
        ),
    ]