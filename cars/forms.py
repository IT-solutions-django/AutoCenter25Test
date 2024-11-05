import re
from django.forms import ModelForm, TextInput, Textarea
from django import forms
from .models import (
    FeedBack,
    Color,
    CarMark,
    Privod
)


class FeedbackForm(ModelForm):
    class Meta:
        model = FeedBack
        fields = ["name", "number", "message"]

        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control fb_name",
                    "placeholder": "Введите имя",
                    "required": "true",
                    "title": "Используйте только буквы",
                }
            ),
            "number": TextInput(
                attrs={
                    "class": "form-control fb_phone",
                    "required": "true",
                    "type": "tel",
                    "placeholder": "+7",
                    "pattern": r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$",
                    "title": "+7 (9XX) XXX-XX-XX",
                }
            ),
            "message": Textarea(
                attrs={
                    "class": "form-control-area",
                    "placeholder": "Введите текст сообщения",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)

        # Удаление id для каждого поля
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["id"] = ""


class CarFilterForm(forms.Form):
    brand = forms.ChoiceField(
        required=False,
        label="Марка",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )
    model = forms.ChoiceField(
        required=False,
        label="Модель",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )

    mileage_min = forms.ChoiceField(
        required=False,
        label="Пробег от",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )

    mileage_max = forms.ChoiceField(
        required=False,
        label="Пробег до",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )

    year_min = forms.ChoiceField(
        required=False,
        label="Год от",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )
    year_max = forms.ChoiceField(
        required=False,
        label="до",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )

    engine_volume_min = forms.ChoiceField(
        required=False,
        label="Объем от",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )
    engine_volume_max = forms.ChoiceField(
        required=False,
        label="до",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )

    transmission = forms.ChoiceField(
        choices=[],
        required=False,
        label="Тип КПП",
        widget=forms.Select(
            attrs={
                "class": "form-control hidden-select"
            },
        ),
    )

    drive = forms.ChoiceField(
        choices=[],
        required=False,
        label="Тип привода",
        widget=forms.Select(
            attrs={
                "class": "form-control hidden-select"
            },
        ),
    )

    color = forms.ChoiceField(
        choices=[],
        required=False,
        label="Цвет",
        widget=forms.Select(
            attrs={
                "class": "form-control hidden-select"
            },
        ),
    )

    rate = forms.ChoiceField(
        required=False,
        label="Рейтинг",
        widget=forms.Select(
            attrs={"class": "form-control hidden-select"},
        ),
    )

    def is_valid(self):
        valid = super(CarFilterForm, self).is_valid()
        if not valid:
            print(self.errors)
            if "model" in self.errors:
                model = self.errors["model"]
                match = re.search(
                    r"Выберите корректный вариант\. (.*?) нет среди допустимых значений\.",
                    model[0],
                )
                value = match.group(1) if match else None
                # value["model"] = value
                self.cleaned_data["model"] = value
                print(value)
                del self.errors["model"]

            if "color" in self.errors:
                color = self.errors["color"]
                match = re.search(
                    r"Выберите корректный вариант\. (.*?) нет среди допустимых значений\.",
                    color[0],
                )
                value = match.group(1) if match else None
                # value["model"] = value
                self.cleaned_data["color"] = value
                print(value)
                del self.errors["color"]

            if "transmission" in self.errors:
                transmission = self.errors["transmission"]
                match = re.search(
                    r"Выберите корректный вариант\. (.*?) нет среди допустимых значений\.",
                    transmission[0],
                )
                value = match.group(1) if match else None
                # value["model"] = value
                self.cleaned_data["transmission"] = value
                print(value)
                del self.errors["transmission"]

            valid = not bool(self.errors)
        return valid


class CarChinaFilterForm(CarFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        brands = CarMark.objects.filter(country='Китай').values_list('id', 'name').order_by('name')

        self.fields["brand"].choices = [("", "Любое")] + list(brands)

        self.fields["model"].choices = [("", "Любое")]

        self.fields["transmission"].choices = [("", "Любое"), (2, 'Автомат'), (1, 'Механика')]

        privods = Privod.objects.all().values_list('id', 'name')

        self.fields["drive"].choices = [("", "Любое")] + list(privods)

        colors = Color.objects.filter(country='Китай').values_list('id', 'name')

        self.fields["color"].choices = [("", "Любое")] + list(colors)

        self.fields['mileage_min'].choices = [("", "Любое")] + [(i, f"{i} км") for i in range(0, 200001, 10000)]

        self.fields['mileage_max'].choices = [("", "Любое")] + [(i, f"{i} км") for i in range(0, 200001, 10000)]

        self.fields['engine_volume_min'].choices = [("", "Любое")] + [(i, f'{i / 1000:.1f}') for i in
                                                                      range(700, 6001, 100)]

        self.fields['engine_volume_max'].choices = [("", "Любое")] + [(i, f'{i / 1000:.1f}') for i in
                                                                      range(700, 6001, 100)]

        self.fields['year_min'].choices = [("", "Любое")] + [(i, i) for i in range(2008, 2025)]

        self.fields['year_max'].choices = [("", "Любое")] + [(i, i) for i in range(2008, 2025)]


class CarJapanFilterForm(CarFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        brands = CarMark.objects.filter(country='Япония').values_list('id', 'name').order_by('name')

        self.fields["brand"].choices = [("", "Любое")] + list(brands)

        self.fields["model"].choices = [("", "Любое")]

        self.fields["transmission"].choices = [("", "Любое"), (2, 'Автомат'), (1, 'Механика')]

        privods = Privod.objects.all().values_list('id', 'name')

        self.fields["drive"].choices = [("", "Любое")] + list(privods)

        colors = Color.objects.filter(country='Япония').values_list('id', 'name')

        self.fields["color"].choices = [("", "Любое")] + list(colors)

        self.fields['mileage_min'].choices = [("", "Любое")] + [(i, f"{i} км") for i in range(0, 200001, 10000)]

        self.fields['mileage_max'].choices = [("", "Любое")] + [(i, f"{i} км") for i in range(0, 200001, 10000)]

        self.fields['engine_volume_min'].choices = [("", "Любое")] + [(i, f'{i / 1000:.1f}') for i in
                                                                      range(700, 6001, 100)]

        self.fields['engine_volume_max'].choices = [("", "Любое")] + [(i, f'{i / 1000:.1f}') for i in
                                                                      range(700, 6001, 100)]

        self.fields['year_min'].choices = [("", "Любое")] + [(i, i) for i in range(2008, 2025)]

        self.fields['year_max'].choices = [("", "Любое")] + [(i, i) for i in range(2008, 2025)]

        self.fields['rate'].choices = [("", "Любое"), ("R", "R"), ("RA", "RA"), ("3", "3"), ("3.5", "3.5"), ("4", "4"),
                                       ("4.", "4."), ("4.5", "4.5"), ("5", "5"), ("6", "6"), ("S", "S")]


class CarKoreaFilterForm(CarFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        brands = CarMark.objects.filter(country='Корея').values_list('id', 'name').order_by('name')

        self.fields["brand"].choices = [("", "Любое")] + list(brands)

        self.fields["model"].choices = [("", "Любое")]

        self.fields["transmission"].choices = [("", "Любое"), (2, 'Автомат'), (1, 'Механика')]

        privods = Privod.objects.all().values_list('id', 'name')

        self.fields["drive"].choices = [("", "Любое")] + list(privods)

        colors = Color.objects.filter(country='Корея').values_list('id', 'name')

        self.fields["color"].choices = [("", "Любое")] + list(colors)

        self.fields['mileage_min'].choices = [("", "Любое")] + [(i, f"{i} км") for i in range(0, 200001, 10000)]

        self.fields['mileage_max'].choices = [("", "Любое")] + [(i, f"{i} км") for i in range(0, 200001, 10000)]

        self.fields['engine_volume_min'].choices = [("", "Любое")] + [(i, f'{i / 1000:.1f}') for i in
                                                                      range(700, 6001, 100)]

        self.fields['engine_volume_max'].choices = [("", "Любое")] + [(i, f'{i / 1000:.1f}') for i in
                                                                      range(700, 6001, 100)]

        self.fields['year_min'].choices = [("", "Любое")] + [(i, i) for i in range(2008, 2025)]

        self.fields['year_max'].choices = [("", "Любое")] + [(i, i) for i in range(2008, 2025)]
