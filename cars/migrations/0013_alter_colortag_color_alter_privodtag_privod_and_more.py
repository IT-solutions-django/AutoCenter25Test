# Generated by Django 5.0.6 on 2024-10-25 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0012_privod_alter_carmark_country_privodtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colortag',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_color', to='cars.color', verbose_name='цвет'),
        ),
        migrations.AlterField(
            model_name='privodtag',
            name='privod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_priv', to='cars.privod'),
        ),
        migrations.CreateModel(
            name='BaseFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100, verbose_name='Страна')),
                ('auction', models.CharField(help_text='исключаем аукционы содержащие эту часть в названии', max_length=20, verbose_name='название аукциона')),
                ('year', models.PositiveIntegerField(help_text='минимальный год для выборки', verbose_name='год выпуска')),
                ('eng_v', models.DecimalField(decimal_places=1, help_text='строго больше какого значения (л)', max_digits=3, verbose_name='объем двигателя')),
                ('mileage', models.PositiveIntegerField(help_text='меньше или равен какому значению', verbose_name='пробег')),
                ('status', models.CharField(blank=True, help_text='строго равен значению', max_length=50, null=True, verbose_name='статус')),
                ('finish', models.PositiveIntegerField(help_text='строго больше какого значения', verbose_name='финиш')),
                ('kpp_type', models.CharField(help_text='берем только эти типы, несколько значений разделяются запятой', max_length=100, verbose_name='типы КПП')),
                ('auction_date', models.PositiveIntegerField(blank=True, help_text='за какой период от текущей даты (дней)', null=True, verbose_name='дата аукциона')),
                ('rate', models.TextField(blank=True, help_text='берем только эти оценки, несколько значений разделяются запятой', null=True, verbose_name='рейтинг')),
                ('marka_name', models.ForeignKey(blank=True, help_text='исключаем эти марки, несколько значений разделяются запятой', null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.carmark', verbose_name='марки автомобиля')),
                ('priv', models.ForeignKey(blank=True, help_text='исключаем эти приводы, несколько значений разделяются запятой', null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.privod', verbose_name='привод автомобиля')),
            ],
            options={
                'verbose_name': 'базовый фильтр',
                'verbose_name_plural': 'базовые фильтры',
            },
        ),
    ]