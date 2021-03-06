# Generated by Django 2.1.5 on 2019-04-20 15:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('username', models.CharField(max_length=32, verbose_name='UserName')),
                ('token', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='Token')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='Mobile Phone')),
                ('level', models.IntegerField(blank=True, choices=[(0, 'View'), (1, 'Exec'), (2, 'Delete')], default=0, verbose_name='User Level')),
                ('avatar', models.CharField(blank=True, default='user.png', max_length=64, verbose_name='User Avatar')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='User Type')),
                ('limit', models.IntegerField(blank=True, default=0, verbose_name='Login Limit')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Create By')),
                ('login_date', models.DateTimeField(blank=True, null=True, verbose_name='Login By')),
                ('valid_date', models.DateTimeField(blank=True, null=True, verbose_name='Valid Date')),
                ('comment', models.CharField(blank=True, max_length=128, null=True, verbose_name='User Comment')),
            ],
            options={
                'verbose_name': 'User Manage',
                'verbose_name_plural': 'User Manage',
                'db_table': 'userprofile',
            },
        ),
        migrations.CreateModel(
            name='DepartMent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='DepartMent Name')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='DepartMent Comment')),
            ],
            options={
                'verbose_name': 'DepartMent Manage',
                'verbose_name_plural': 'DepartMent Manage',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='KeyManage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Key Name')),
                ('user', models.CharField(blank=True, max_length=64, null=True, verbose_name='Key User')),
                ('password', models.CharField(blank=True, max_length=64, null=True, verbose_name='Key Password')),
                ('private', models.TextField(verbose_name='Private Key')),
                ('public', models.TextField(verbose_name='Public Key')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create By')),
            ],
            options={
                'verbose_name': 'Key Manage',
                'verbose_name_plural': 'Key Manage',
                'db_table': 'keymanage',
            },
        ),
        migrations.CreateModel(
            name='MenuList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='Menu Name')),
                ('first', models.CharField(blank=True, max_length=32, null=True, verbose_name='First Menu')),
                ('secondary', models.CharField(blank=True, default='Nothing', max_length=32, null=True, verbose_name='Secondary Menu')),
            ],
            options={
                'verbose_name': 'Menu Manage',
                'verbose_name_plural': 'Menu Manage',
                'db_table': 'menuList',
            },
        ),
        migrations.CreateModel(
            name='PermissionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Permission Name')),
                ('lable_name', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Permission Lable')),
                ('url', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Permission Url')),
                ('menu', models.ManyToManyField(blank=True, to='users.MenuList', verbose_name='Menu Manager')),
            ],
            options={
                'verbose_name': 'Permission Manage',
                'verbose_name_plural': 'Permission Manage',
                'db_table': 'permissionList',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Project Name')),
                ('mini_name', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='Project MiniName')),
                ('create_date', models.DateField(auto_now_add=True, null=True, verbose_name='Create By')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Project Comment')),
                ('key', models.ManyToManyField(blank=True, to='users.KeyManage', verbose_name='Project Keyfile')),
            ],
            options={
                'verbose_name': 'Project Manage',
                'verbose_name_plural': 'Project Manage',
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='RoleList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='RoleName')),
                ('permission', models.ManyToManyField(blank=True, to='users.PermissionList', verbose_name='Permission List')),
            ],
            options={
                'verbose_name': 'Role Manage',
                'verbose_name_plural': 'Role Manage',
                'db_table': 'rolelist',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.DepartMent', verbose_name='User Department'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='project',
            field=models.ManyToManyField(blank=True, default=None, to='users.Project', verbose_name='User Project'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.RoleList', verbose_name='User Role'),
        ),
    ]
