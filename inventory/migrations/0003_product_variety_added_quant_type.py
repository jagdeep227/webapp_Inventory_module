# Generated by Django 3.1.1 on 2020-09-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20200922_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_variety_added',
            name='quant_type',
            field=models.CharField(default='kg', max_length=50),
        ),
    ]