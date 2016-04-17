from django.template.defaultfilters import register


@register.filter
def subtract(value, arg):
    return value - arg
