# Generated by Django 3.0.6 on 2020-06-19 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shops', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopaddress',
            old_name='Longitude',
            new_name='longitude',
        ),
        migrations.RemoveField(
            model_name='shopdetails',
            name='staffs',
        ),
    ]
