# Generated by Django 5.0.6 on 2024-10-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0015_remove_carmainpage_body_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='reviews_date',
            field=models.DateField(blank=True, help_text='Уже загруженные фотографии не нужно добовлять заново', null=True, verbose_name='Дата отзыва'),
        ),
    ]
