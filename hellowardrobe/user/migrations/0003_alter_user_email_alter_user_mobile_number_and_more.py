# Generated by Django 4.1.3 on 2023-04-25 09:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, db_index=True, default=None, max_length=254, null=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(db_index=True, error_messages={'unique': 'User already exists. Please use a different mobile number'}, max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Invalid mobile number')]),
        ),
        migrations.AlterField(
            model_name='userotp',
            name='mobile',
            field=models.CharField(db_index=True, max_length=10, unique=True, verbose_name='Mobile Number'),
        ),
    ]
