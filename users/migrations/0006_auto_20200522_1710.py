# Generated by Django 3.0.6 on 2020-05-22 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20200522_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
