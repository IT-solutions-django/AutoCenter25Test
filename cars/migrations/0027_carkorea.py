# Generated by Django 5.0.6 on 2024-11-10 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0026_alter_carmainpage_color_alter_carmainpage_drive_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarKorea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(help_text='Впишите название бренда', max_length=100, verbose_name='Бренд')),
                ('model', models.CharField(help_text='Впишите название модели', max_length=150, verbose_name='Модель')),
                ('year', models.IntegerField(help_text='Впишите год автомабиля', verbose_name='Год')),
                ('engine_volume', models.IntegerField(help_text='Впишите объяем двигателя', verbose_name='Объяем двигателя')),
                ('mileage', models.IntegerField()),
                ('price', models.IntegerField()),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.colormainpagecars', verbose_name='Цвет')),
                ('drive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.drive', verbose_name='Тип привода')),
                ('photos', models.ManyToManyField(null=True, to='cars.photocars', verbose_name='Фотографии авто')),
            ],
            options={
                'verbose_name': 'Авто Корея',
                'verbose_name_plural': 'Авто Корея',
            },
        ),
    ]