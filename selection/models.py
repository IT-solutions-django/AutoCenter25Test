from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='заголовок'
    )

    class Meta:
        verbose_name = "заголовок для страницы 'Автоподбор'"
        verbose_name_plural = "заголовки для страницы 'Автоподбор'"

    def __str__(self):
        return self.name


class Selection(models.Model):
    name = models.TextField(
        verbose_name='название'
    )
    description = models.TextField(
        verbose_name='описание',
        null=True,
        blank=True
    )
    price = models.CharField(
        max_length=100,
        verbose_name='стоимость',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория'
    )

    class Meta:
        verbose_name = "данные к странице 'Автоподбор'"
        verbose_name_plural = "данные к странице 'Автоподбор'"

    def __str__(self):
        return self.name
