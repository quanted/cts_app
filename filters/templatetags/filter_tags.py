"""
Filters for getting class names and
field types from the form
"""
from django import template
from django.forms import CheckboxInput
import logging

register = template.Library()

@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__

@register.filter(name='is_checkbox')
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

# labelDict = { "cts_aerobic" : "Aerobic", "cts_anaerobic" : "Anaerobic" }
# @register.filter(name='class_label')
# def class_label(form):
# 	key = form.__class__.__name__ # get class name as key
# 	if key in labelDict:
# 		return labelDict[key]
# 	else:
# 		return key

@register.filter(name='widget_type')
def widget_type(field):
	return field.field.widget.__class__.__name__

# @register.filter(name='add_class')
# def add_class(field, class_name):
# 	logging.warning(field)
# 	return field.as_widget(attrs={"class":class_name})