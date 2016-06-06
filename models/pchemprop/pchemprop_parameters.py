# -*- coding: utf-8 -*-
"""
@author: (np)
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms, template
from django.db import models	
from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging
from django.template.defaultfilters import stringfilter
from django.core import validators
from models.forms import validation
from filters.templatetags import color_table
from parsley.decorators import parsleyfy


# Define Custom Templates
def tmpl_pchemTableCTS():
	tmpl_pchemTableCTS = """
	{% load color_table %}
	{% for field in form %}
		{% if field.id_for_label == "id_kow_wph" %}
			<tr>
			<th class="chemprop">{{ field }} <span>{{ field.label }}</span>
		{% elif field.id_for_label == "id_kow_ph" %}
			<span>{{field.label}}</span> {{field}}<br><div style="float:right;">{{field.errors}}</div></th>
			<td id="id_kow_ChemAxon" class="{{form.kow_wph|color_filter:"chemaxon"}} chemaxon kow_wph"></td>
			<td id="id_kow_EPI" class="{{form.kow_wph|color_filter:"epi"}} epi kow_wph"></td>
			<td id="id_kow_TEST" class="{{form.kow_wph|color_filter:"test"}} test kow_wph"></td>
			<td id="id_kow_SPARC" class="{{form.kow_wph|color_filter:"sparc"}} sparc kow_wph"></td>
			<td id="id_kow_Measured" class="{{form.kow_wph|color_filter:"measured"}} measured kow_wph"></td>
		{% elif field.id_for_label != "id_nodes" %}
			<tr>
			<th class="chemprop">{{ field }} <span>{{ field.label }}</span></th>
			<td id="{{ field.id_for_label }}_ChemAxon" class="{{ field | color_filter:"chemaxon" }} chemaxon {{field.name}}"></td>
			<td id="{{ field.id_for_label }}_EPI" class="{{ field | color_filter:"epi" }} epi {{field.name}}"></td>
			<td id="{{ field.id_for_label }}_TEST" class="{{ field | color_filter:"test" }} test {{field.name}}"></td>
			<td id="{{ field.id_for_label }}_SPARC" class="{{ field | color_filter:"sparc" }} sparc {{field.name}}"></td>
			<td id="{{ field.id_for_label }}_Measured" class="{{ field | color_filter:"measured" }} measured {{field.name}}"></td>
			</tr>
		{% endif %}
	{% endfor %}
		<tr>
			<th></th>
			<td class="ChemCalcs_available colorKey">Available</td>
			<td class="ChemCalcs_unavailable colorKey">Unavailable</td>
		</tr>
	</table>

	"""
	return tmpl_pchemTableCTS


tmpl_pchemTableCTS = Template(tmpl_pchemTableCTS())


# Method(s) called from *_inputs.py
def form(formData):
	form_cts_ChemCalcs_props = CTS_ChemCalcs_Props(formData)
	html = tmpl_pchemTableCTS.render(Context(dict(form=form_cts_ChemCalcs_props)))
	return html


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
	koc = forms.BooleanField(required=False, label=mark_safe('Organic Carbon Partition Coefficient (L/kg)'))


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
		calcDict = dict(zip(color_table.props_list, color_table.chemaxon_props))
	elif calculator == "epi":
		calcDict = dict(zip(color_table.props_list, color_table.epi_props))
	elif calculator == "test":
		calcDict = dict(zip(color_table.props_list, color_table.test_props))
	elif calculator == "sparc":
		calcDict = dict(zip(color_table.props_list, color_table.sparc_props))
	elif calculator == "measured":
		calcDict = dict(zip(color_table.props_list, color_table.measured_props))

	available = None
	if prop in calcDict:
		if 'unavailable' in calcDict[prop]:
			available = False
		else:
			available = True
	return available
