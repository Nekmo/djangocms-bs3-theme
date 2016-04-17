from django.template.defaultfilters import register


@register.filter
def only_file_name(value):
    value = value.split('/')[-1]
    return value.split('.')[0]
