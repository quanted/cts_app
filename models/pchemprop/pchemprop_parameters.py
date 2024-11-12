# -*- coding: utf-8 -*-
"""
@author: (np)
"""
from django import forms, template
from django.db import models	
from django.template import Context, Template
from django.utils.safestring import mark_safe
from parsley.decorators import parsleyfy


# Temporarily moved here from filters/templatetags/color_table.py in order to remove
# that folder entirely.
# TODO: Consider using calculators' props attribute in pchempropAvailable() below
####################################################################################



# NOTE: This stuff should all be in the calculator classes so it's definied in one place.
available_props = {
	"chemaxon": ["water_sol", "ion_con", "kow_no_ph", "kow_wph", "water_sol_ph"],
	"epi": ["melting_point", "boiling_point", "water_sol", "vapor_press", "henrys_law_con", "kow_no_ph", "koc", "log_bcf", "log_baf"],
	"test": ["melting_point", "boiling_point", "water_sol", "vapor_press", "log_bcf"],
	"equation": ["mol_diss", "mol_diss_air"],
	"measured": ["melting_point", "boiling_point", "water_sol", "vapor_press", "henrys_law_con", "kow_no_ph", "koc", "log_bcf", "log_baf"],
	"opera": ["melting_point", "boiling_point", "water_sol", "vapor_press", "ion_con", "henrys_law_con", "kow_no_ph", "koc", "log_bcf", "kow_wph"]
}


# Method(s) called from *_inputs.py
def form(formData):
	# form_cts_ChemCalcs_props = CTS_ChemCalcs_Props(formData)
	# html = tmpl_pchemTableCTS.render(Context(dict(form=form_cts_ChemCalcs_props)))
	# return html
	return ""


@parsleyfy
class CTS_ChemCalcs_Props(forms.Form):
	melting_point = forms.BooleanField(required=False, label=mark_safe('Melting Point (&degC)'))
	boiling_point = forms.BooleanField(required=False, label=mark_safe('Boiling Point (&degC)'))
	water_sol = forms.BooleanField(required=False, label=mark_safe('Water Solubility (mg/L)'))
	vapor_press = forms.BooleanField(required=False, label=mark_safe('Vapor Pressure (mmHg)'))
	mol_diss = forms.BooleanField(required=False, label=mark_safe('Molecular Diffusivity (cm<sup>2</sup>/s)'))
	ion_con = forms.BooleanField(required=False, label=mark_safe('Ionization Constant'))
	henrys_law_con = forms.BooleanField(required=False, label=mark_safe("Henry's Law Constant (atm-m<sup>3</sup>/mol)"))
	kow_no_ph = forms.BooleanField(required=False, label=mark_safe("Octanol/Water Partition Coefficient (log)"))
	kow_wph = forms.BooleanField(required=False, label=mark_safe('Octanol/Water Partition Coefficient (log)'))
	kow_ph = forms.DecimalField (
				label='at pH:',
				widget=forms.NumberInput(attrs={'class':'numberInput'}),
				initial=7.4,
				min_value=0,
				max_value=14,
				decimal_places=1,
				max_digits=4
			)
	koc = forms.BooleanField(required=False, label=mark_safe('Organic Carbon Partition Coefficient (log)'))


class PchempropInp(CTS_ChemCalcs_Props):
	pass


def pchempropAvailable(calculator, prop):
	"""
	Checks availability of chemical property 
	for a given calculator
	Inputs:
	calculator - (string) e.g., "chemaxon", "equation", etc.
	prop - (string) chemical property same as id, e.g., "melting_point", "ion_con", etc.
	Returns: (boolean) whether prop is available for that calculator.
	"""

	calc_props = available_props.get(calculator)

	if not calc_props:
		return False

	if prop in calc_props:
		return True
	else:
		return False
