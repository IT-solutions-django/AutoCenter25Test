from django.db import models


class About(models.Model):
    phone = models.CharField(
        max_length=50,
        verbose_name='номер телефона'
    )
    email = models.EmailField()
    working_days = models.CharField(
        max_length=100,
        verbose_name='рабочие дни'
    )
    working_time = models.CharField(
        max_length=100,
        verbose_name='рабочие часы'
    )
    weekends = models.CharField(
        max_length=100,
        verbose_name='выходные дни'
    )
    address = models.TextField(
        verbose_name='адрес офиса'
    )
    current_account = models.CharField(
        max_length=100,
        verbose_name='расчётный счёт'
    )
    name_bank = models.CharField(
        max_length=100,
        verbose_name='название банка'
    )
    bik = models.CharField(
        max_length=100,
        verbose_name='БИК'
    )
    correspondent_account = models.CharField(
        max_length=100,
        verbose_name='корреспондентский счёт'
    )
    denomination = models.TextField(
        verbose_name='наименование'
    )
    inn = models.CharField(
        max_length=100,
        verbose_name='ИНН/КПП'
    )
    ogrn = models.CharField(
        max_length=100,
        verbose_name='ОГРН'
    )
    gis = models.URLField(
        verbose_name='2GIS',
        null=True
    )
    yandex_map = models.URLField(
        verbose_name='яндекс карты',
        null=True
    )

    class Meta:
        verbose_name = "страница 'О нас'"
        verbose_name_plural = "страница 'О нас'"

    def __str__(self):
        return self.denomination
