# Generated by Django 5.0.6 on 2024-11-10 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0021_basefilter_max_eng_v'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='тип кузова')),
            ],
            options={
                'verbose_name': 'тип кузова',
                'verbose_name_plural': 'типы кузова',
            },
        ),
    ]
