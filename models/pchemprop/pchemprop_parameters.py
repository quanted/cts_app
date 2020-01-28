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
props_list = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss', 'ion_con',
			'henrys_law_con', 'kow_no_ph', 'kow_wph', 'koc', 'water_sol_ph', 'log_bcf', 'log_baf', 'mol_diss_air']

# List of each provider's available properties (see props list):
chemaxon_props = ['ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 
					'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']

# NOTE: temporarily setting koc for epi to unavailable
epi_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable']

# NOTE: temporarily setting kow_no_ph for test to unavailable
test_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
 				'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']

sparc_props = ['ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available']

# NOTE: Measured data is from EPI measured values
measured_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']

opera_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available',
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']
####################################################################################



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
	calculator - (string) e.g., "chemaxon", "sparc", etc.
	prop - (string) chemical property same as id, e.g., "melting_point", "ion_con", etc.
	Returns: (boolean) whether prop is available for that calculator.
	"""

	calcDict = {}

	if calculator == "chemaxon":
		calcDict = dict(zip(props_list, chemaxon_props))
	elif calculator == "epi":
		calcDict = dict(zip(props_list, epi_props))
	elif calculator == "test":
		calcDict = dict(zip(props_list, test_props))
	elif calculator == "sparc":
		calcDict = dict(zip(props_list, sparc_props))
	elif calculator == "measured":
		calcDict = dict(zip(props_list, measured_props))
	elif calculator == "opera":
		calcDict = dict(zip(props_list, opera_props))

	if prop in calcDict:
		if 'unavailable' in calcDict[prop]:
			return False
		else:
			return True

	return False
