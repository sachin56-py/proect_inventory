# Generated by Django 4.1.4 on 2022-12-18 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0002_alter_item_added_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='added_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 18, 19, 43, 28, 413798)),
        ),
    ]
