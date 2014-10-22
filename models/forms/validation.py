# -*- coding: utf-8 -*-

"""
.. module:: validation
   :synopsis: Our custom defined Django validation rules
"""

from django.core.exceptions import ValidationError
import logging

# Built-in Django validation rules

#
# validate_slug - A RegexValidator instance that ensures a value consists of only letters, numbers, underscores or hyphens. NOTE: Does not allow spaces
#
# validate_integer - Raises a ValidationError if value fails 'value(int)'.
#
# max_value - Raises a ValidationError with a code of 'max_value' if value is greater than max_value.
#
# min_value - Raises a ValidationError with a code of 'min_value' if value is less than min_value.
#
# max_length - Raises a ValidationError with a code of 'max_length' if the length of value is greater than max_length.
#
# min_length - Raises a ValidationError with a code of 'min_length' if the length of value is less than min_length.
#
# validate_email - A RegexValidator instance that ensures a value looks like an email address.
#
# validate_comma_separated_integer_list - A RegexValidator instance that ensures a value is a comma-separated list of integers.
#
# URLValidator - A RegexValidator that ensures a value looks like a URL, and raises an error code of 'invalid' if it doesn’t.
#
# validate_ipv4_address - A RegexValidator instance that ensures a value looks like an IPv4 address.
#
# validate_ipv6_address - Uses django.utils.ipv6 to check the validity of an IPv6 address.
#
# validate_ipv46_address - Uses both validate_ipv4_address and validate_ipv6_address to ensure a value is either a valid IPv4 or IPv6 address.
#


def validate_range01(value):
	""" Form Validation Rule: Valid range 0 - 1
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if 0 <= value <= 1:
		pass
	else:
		raise ValidationError(u'Range must fall between 0 - 1')

def validate_range0100(value):
	""" Form Validation Rule: Valid range 0 - 100 (e.g. temperature Centigrade/Celsius)
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if 0 <= value <= 100:
		pass
	else:
		raise ValidationError(u'Range must fall between 0 - 100')

def validate_range_1_365(value):
	""" Form Validation Rule: Valid range 1 - 365 (e.g. Day of the Year)
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if 1 <= value <= 365:
		pass
	else:
		raise ValidationError(u'Range must fall between 1 - 365')

def validate_integer(value):
	""" Form Validation Rule: Valid if integer
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if int(value) == value:
		pass
	else:
		raise ValidationError(u'Value must be an integer')

def validate_greaterthan0(value):
	""" Form Validation Rule: Valid if value > 0
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if value > 0:
		pass
	else:
		raise ValidationError(u'Value must be greater than 0')

def validate_positive(value):
	""" Form Validation Rule: Valid if value is positive (>= 0)
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if value < 0:
		raise ValidationError(u'Value must be positive')

def validate_greaterthanequalto1(value):
	""" Form Validation Rule: Valid if value >= 1 (e.g. Mineau scaling factor)
	
	:param value: Form input field value
	:raises: ValidationError
	"""
	if value < 1:
		raise ValidationError(u'Value must greater than or equal to 1')

def validate_choicefield(value):
	""" Form Validation Rule: ChoiceField (drop-down menu), value is not 0 (e.g. "Make a selection")

	:param value: Form input field value
	:raises: ValidationError
	"""
	if value == "0" or value == 0:
		raise ValidationError(u'Make a selection')

def validate_degrees_latitude(value):
	""" Form Validation Rule: Degrees Latitue (-90 to 90)

	:param value: Form input field value
	:raises: ValidationError
	"""
	if -90 <= value <= 90:
		pass
	else:
		raise ValidationError(u'Range between -90 and 90')

def validate_number(value):
	""" Form Validation Rule: value must be int or dbl, and
		value must go < 2 decimals places to the right

	:param value: form input field value
	:raises: ValidationError
	"""
	# if int(value) == value or float(value) == value:
	# if not value:
	# 	raise ValidationError(u'value must not be blank')
	# logging.warning('VALUE: ' + str(value))

	if int(value) == value:
		pass
	else:
		raise ValidationError(u'value must be a number')

# def validate_existence(value):
# 	""" Form Validation rule: value must not be blank

# 	:param value: form input field value
# 	:raises: ValidationError
# 	"""
# 	logging.warning("INSIDE VALIDATE EXISTENCE")

# 	if value:
# 		pass
# 	else:
# 		raise ValidationError(u'value must not be blank')