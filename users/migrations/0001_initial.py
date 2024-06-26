# Generated by Django 3.0.6 on 2020-05-20 14:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, null=True, verbose_name='Address line 2')),
                ('land_mark', models.CharField(max_length=1024, null=True, verbose_name='Land mark')),
                ('latitude', models.CharField(max_length=255, verbose_name='Latitude')),
                ('longitude', models.CharField(max_length=255, verbose_name='Latitude')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('state', models.CharField(max_length=20, verbose_name='State')),
                ('country', models.CharField(max_length=20, verbose_name='Country')),
            ],
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('blocked', 'blocked')], default='active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=10)),
                ('created_by', models.CharField(default=None, max_length=255, null=True)),
                ('address', models.ManyToManyField(default=None, null=True, to='users.Address')),
                ('pages', models.ManyToManyField(default=None, null=True, to='users.Pages')),
                ('role', models.ManyToManyField(default=None, null=True, to='users.UserRoles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
