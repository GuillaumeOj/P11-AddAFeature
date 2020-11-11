from django import template
from django.http import QueryDict

register = template.Library()


@register.filter(name="add_attrs")
def add_attrs(field, attrs):
    # Transform attributes in a Python dict
    attrs = dict(QueryDict(query_string=attrs, mutable=True))

    # Transform each dict item in a str instead of a list
    for attr, value in attrs.items():
        attrs[attr] = " ".join(value)
    return field.as_widget(attrs=attrs)
