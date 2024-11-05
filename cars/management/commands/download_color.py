import json

from django.core.management.base import BaseCommand, CommandError

from cars.models import Color, ColorTag


class Command(BaseCommand):
    """
    Команда для скачивания цветов.
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument("country", type=str)

    def handle(self, *args, **options):
        try:
            with open(options["file_path"], "r", encoding="utf-8") as file:
                colors_data = json.load(file)

            country = options["country"]
            for color in colors_data:
                current_color, _ = Color.objects.get_or_create(
                    name=color["name"], country=country
                )
                for current_color_tag in color["colors"]:
                    ColorTag.objects.get_or_create(
                        name=current_color_tag,
                        color=current_color,
                    )

        except Exception as e:
            raise CommandError(e)
        else:
            self.stdout.write(self.style.SUCCESS("Colors Downloading success"))
