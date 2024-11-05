import uuid
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse


class PhotoCars(models.Model):
    image = models.ImageField(upload_to="photos/")

    def save(self, *args, **kwargs):
        name = str(uuid.uuid1())
        img = Image.open(self.image)
        img_io = BytesIO()
        img.save(img_io, format="WebP")
        img_file = InMemoryUploadedFile(
            img_io, None, f"{name}.webp", "image/webp", img_io.tell(), None
        )
        self.image.save(f"{name}.webp", img_file, save=False)

        super(PhotoCars, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Фото машины")
        verbose_name_plural = _("Фото машин")

    def __str__(self):
        return f"{self.image}"


class Reviews(models.Model):
    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    name = models.CharField(
        max_length=200,
        verbose_name=_("Имя Фамилия"),
    )

    text_review = models.TextField(verbose_name=_("Коментарий пользователя"))

    icon_user = models.CharField(
        max_length=200,
        null=True,
        verbose_name=_("Фотографии пользователя"),
    )

    num_view = models.IntegerField(
        verbose_name=_("Номер отображения"),
        help_text=_("Каким по очереди отображать?"),
        default=0,
    )

    image1 = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("Фотография к отзыву 1"),
    )

    image2 = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("Фотография к отзыву 2"),
    )

    # def save(self, *args, **kwargs):
    #     if self.icon_user:
    #         name = str(uuid.uuid1())
    #         img = Image.open(self.icon_user)
    #         img_io = BytesIO()
    #         img.save(img_io, format="WebP")
    #         img_file = InMemoryUploadedFile(
    #             img_io, None, f"{name}.webp", "image/webp", img_io.tell(), None
    #         )
    #         self.icon_user.save(f"{name}.webp", img_file, save=False)
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class FeedBack(models.Model):
    name = models.CharField("Имя", max_length=50)
    number = models.CharField("Номер телефона", max_length=20, validators=[MinLengthValidator(18)])
    message = models.TextField("Сообщение", blank=True, null=True)

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} {self.number}"

    class Meta:
        verbose_name = "Завяка"
        verbose_name_plural = "Заявки"


class Color(models.Model):
    class Meta:
        verbose_name = _("Цвет для машины")
        verbose_name_plural = _("Цвета для машин")

    country = models.CharField(verbose_name=_("Страна"), max_length=100, default="Япония")
    name = models.CharField(verbose_name=_("Название цвета"), max_length=100)

    def __str__(self):
        return f"{self.name}"


class ColorTag(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name="tags_color", verbose_name="цвет"
    )

    class Meta:
        verbose_name = _("Тег для цвета")
        verbose_name_plural = _("Теги для цветов")

    def __str__(self):
        return self.name


class CarMainPage(models.Model):
    class Meta:
        verbose_name = "Авто Главная Страница"
        verbose_name_plural = "Авто Главная Страница"

    brand = models.CharField(
        max_length=100,
        verbose_name=_("Бренд"),
        help_text=_("Впишите название бренда"),
    )
    model = models.CharField(
        max_length=150,
        verbose_name=_("Модель"),
        help_text=_("Впишите название модели"),
    )
    year = models.IntegerField(
        verbose_name=_("Год"), help_text=_("Впишите год автомабиля")
    )
    transmission = models.CharField(
        max_length=150, verbose_name=_("Тип КПП"),
        help_text=_("Автомат или Механика")
    )
    engine_volume = models.IntegerField(
        verbose_name=_("Объяем двигателя"),
        help_text=_("Впишите объяем двигателя"),
    )
    drive = models.ForeignKey(
        "Privod", on_delete=models.CASCADE, verbose_name=_("Тип привода")
    )
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, verbose_name=_("Цвет")
    )
    mileage = models.IntegerField()
    price = models.IntegerField()

    photos = models.ManyToManyField(
        PhotoCars, null=True, verbose_name=_("Фотографии авто")
    )

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) {self.color} - {self.price}"

    def get_absolute_url(self):
        return reverse("car_main_page/", kwargs={"pk": self.pk})


class Currency(models.Model):
    class Meta:
        verbose_name = "Валюты"
        verbose_name_plural = "Валюты"

    date = models.CharField(
        max_length=100,
        verbose_name=_("Дата парсинга"),
    )

    usd = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("USD"),
    )

    eur = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("EUR"),
    )

    jpy = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("JPY"),
    )

    krw = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("KRW"),
    )

    cny = models.FloatField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("CNY"),
    )

    def __str__(self):
        return f"{self.date}"


class CarMark(models.Model):
    country = models.CharField(verbose_name=_("Страна"), max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Уникальные марки авто")
        verbose_name_plural = _("Уникальные марки авто")

    def __str__(self):
        return f"{self.name} | {self.country}"


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    mark = models.ForeignKey(CarMark, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Уникальные модели авто")
        verbose_name_plural = _("Уникальные модели авто")

    def __str__(self):
        return f"{self.name}"


class Privod(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Привод авто")
        verbose_name_plural = _("Приводы авто")

    def __str__(self):
        return f"{self.name}"


class PrivodTag(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="название",
        help_text="максимальная длина 255 символов",
    )
    privod = models.ForeignKey(
        Privod, on_delete=models.CASCADE, related_name="tags_priv"
    )

    class Meta:
        verbose_name = _("Тег для привода")
        verbose_name_plural = _("Теги для приводов")

    def __str__(self):
        return self.name


class BaseFilter(models.Model):
    country = models.CharField(verbose_name=_("Страна"), max_length=100)
    auction = models.CharField(
        max_length=20,
        verbose_name="название аукциона",
        help_text="исключаем аукционы содержащие эту часть в названии",
    )
    marka_name = models.TextField(
        verbose_name="марки автомобиля",
        help_text="исключаем эти марки, несколько значений разделяются запятой",
        blank=True,
        null=True,
    )
    year = models.PositiveIntegerField(
        verbose_name="год выпуска",
        help_text="минимальный год для выборки",
    )
    eng_v = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name="объем двигателя",
        help_text="строго больше какого значения (л)",
    )
    mileage = models.PositiveIntegerField(
        verbose_name="пробег",
        help_text="меньше или равен какому значению",
    )
    status = models.CharField(
        max_length=50,
        verbose_name="статус",
        help_text="строго равен значению",
        blank=True,
        null=True,
    )
    priv = models.TextField(
        verbose_name="привод автомобиля",
        help_text="исключаем эти приводы, несколько значений разделяются запятой",
        blank=True,
        null=True,
    )
    finish = models.PositiveIntegerField(
        verbose_name="финиш",
        help_text="строго больше какого значения",
    )
    kpp_type = models.CharField(
        max_length=100,
        verbose_name="типы КПП",
        help_text="берем только эти типы, несколько значений разделяются запятой",
    )
    auction_date = models.PositiveIntegerField(
        verbose_name="дата аукциона",
        help_text="за какой период от текущей даты (дней)",
        blank=True,
        null=True,
    )
    rate = models.TextField(
        verbose_name="рейтинг",
        help_text="берем только эти оценки, несколько значений разделяются запятой",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "базовый фильтр"
        verbose_name_plural = "базовые фильтры"

    def __str__(self):
        return self.country
