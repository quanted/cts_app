"""
Filters for getting class names and
field types from the form
"""
from django import template
from django.forms import CheckboxInput

register = template.Library()

@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__

@register.filter(name='is_checkbox')
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__