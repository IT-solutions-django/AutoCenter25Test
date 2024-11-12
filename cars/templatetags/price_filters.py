from django import template

register = template.Library()


@register.filter
def format_price(value):
    return '{:,}'.format(int(value)).replace(',', ' ')


@register.filter
def multiply(value, arg):
    return float(value) * float(arg)


@register.filter
def percentage(value, perc):
    return float(value) / 100 * perc
