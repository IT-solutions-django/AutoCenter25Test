# Generated by Django 5.0.6 on 2024-11-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0024_drive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='тип кпп')),
            ],
            options={
                'verbose_name': 'тип кпп для популярных машин',
                'verbose_name_plural': 'типы кпп для популярных машин',
            },
        ),
        migrations.CreateModel(
            name='TypeEngine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='тип двигателя')),
            ],
            options={
                'verbose_name': 'тип двигателя для популярных машин',
                'verbose_name_plural': 'типы двигателей для популярных машин',
            },
        ),
    ]
