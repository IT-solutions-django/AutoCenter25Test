# Generated by Django 5.0.6 on 2024-10-28 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0019_alter_reviews_icon_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='icon_user',
            field=models.CharField(max_length=200, null=True, verbose_name='Фотографии пользователя'),
        ),
    ]