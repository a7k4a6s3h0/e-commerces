# Generated by Django 4.1 on 2022-11-17 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondapp', '0004_remove_add_product_cupen_reduced_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_product',
            name='stock',
            field=models.IntegerField(),
        ),
    ]
