# Generated by Django 5.0.6 on 2024-11-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50, verbose_name='номер телефона')),
                ('email', models.EmailField(max_length=254)),
                ('working_days', models.CharField(max_length=100, verbose_name='рабочие дни')),
                ('working_time', models.CharField(max_length=100, verbose_name='рабочие часы')),
                ('weekends', models.CharField(max_length=100, verbose_name='выходные дни')),
                ('address', models.CharField(max_length=500, verbose_name='адрес офиса')),
                ('current_account', models.CharField(max_length=100, verbose_name='расчётный счёт')),
                ('name_bank', models.CharField(max_length=100, verbose_name='название банка')),
                ('bik', models.CharField(max_length=100, verbose_name='БИК')),
                ('correspondent_account', models.CharField(max_length=100, verbose_name='корреспондентский счёт')),
                ('denomination', models.CharField(max_length=500, verbose_name='наименование')),
                ('inn', models.CharField(max_length=100, verbose_name='ИНН/КПП')),
                ('ogrn', models.CharField(max_length=100, verbose_name='ОГРН')),
            ],
            options={
                'verbose_name': "страница 'О нас'",
                'verbose_name_plural': "страница 'О нас'",
            },
        ),
    ]