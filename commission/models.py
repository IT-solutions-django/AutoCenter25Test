from django.db import models


class Commission(models.Model):
    commission_storage = models.PositiveIntegerField(
        verbose_name="Склад, ЭПТС СБКТС, Услуга оформления",
        help_text="в рублях",
    )
    commission_broker = models.PositiveIntegerField(
        verbose_name="Перегон и сопутствующие регистрации",
        help_text="в рублях",
    )
    commission = models.PositiveIntegerField(
        verbose_name="комиссия", help_text="в рублях"
    )
    commission_delivery = models.PositiveIntegerField(
        verbose_name="комиссия в валюте экспортера",
        help_text="в валюте страны экспортера",
    )
    japan_sanction_percent = models.PositiveIntegerField(
        verbose_name="Процент комиссии Японских санкционных авто",
        help_text="в процентах",
        blank=True,
        null=True,
    )
    japan_sanction_commission = models.PositiveIntegerField(
        verbose_name="комиссия в валюте экспортера для Японских санкционных авто",
        help_text="в валюте страны экспортера",
        blank=True,
        null=True,
    )
    korea_sanction_commission = models.PositiveIntegerField(
        verbose_name="комиссия в валюте экспортера для Корейских авто стоимостью выше 30 млн Вон",
        help_text="в валюте страны экспортера",
        blank=True,
        null=True,
    )

    country = models.CharField(
        max_length=100,
        verbose_name="страна",
    )

    class Meta:
        verbose_name = "комиссия"
        verbose_name_plural = "комиссии"
        ordering = ("country",)

    def __str__(self):
        return f"Комиссия из {self.country}"
