# Generated by Django 5.0.6 on 2024-10-23 15:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_alter_feedback_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='number',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='Номер телефона'),
        ),
    ]
