# Generated by Django 5.0.6 on 2024-10-28 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0018_alter_reviews_icon_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='icon_user',
            field=models.ImageField(null=True, upload_to='user/phoro_user', verbose_name='Фотографии пользователя'),
        ),
    ]
