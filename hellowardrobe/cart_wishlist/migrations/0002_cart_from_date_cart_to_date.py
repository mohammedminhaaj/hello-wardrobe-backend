# Generated by Django 4.1.3 on 2023-05-02 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 11, 27, 57, 263615, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 11, 28, 13, 229062, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
