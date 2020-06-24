# Generated by Django 3.0.6 on 2020-06-19 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shops', '0002_auto_20200619_0845'),
        ('users', '0008_userdetails_referance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='address',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='pages',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='role',
        ),
        migrations.RemoveField(
            model_name='userroles',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userroles',
            name='status',
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userroles',
            name='role',
            field=models.CharField(choices=[('delivery', 'delivery'), ('order_management', 'order_management'), ('stock_management', 'stock_management')], default=None, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userroles',
            name='shop',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Shops.ShopDetails'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userroles',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Pages',
        ),
    ]
