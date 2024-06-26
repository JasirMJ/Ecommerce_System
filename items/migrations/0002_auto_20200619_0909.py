# Generated by Django 3.0.6 on 2020-06-19 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shops', '0002_auto_20200619_0845'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblinventory',
            name='shop',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Shops.ShopDetails'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblitemcategory',
            name='shop',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Shops.ShopDetails'),
            preserve_default=False,
        ),
    ]
