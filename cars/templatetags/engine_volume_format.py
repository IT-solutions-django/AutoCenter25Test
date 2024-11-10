from django import template

register = template.Library()


@register.filter
def engine_volume_format(value):
    return f"{value / 1000:.2f}"[:-1]
