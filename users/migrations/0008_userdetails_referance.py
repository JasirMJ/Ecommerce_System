# Generated by Django 3.0.6 on 2020-05-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200523_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='referance',
            field=models.CharField(default=None, max_length=6, null=True),
        ),
    ]