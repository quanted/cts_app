# -*- coding: utf-8 -*-
"""
@author: J.Flaishans
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms, template
from django.db import models	
from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging
from django.template.defaultfilters import stringfilter


# Define Custom Templates
def tmpl_ChemCalcsCTS():
	tmpl_ChemCalcsCTS = """
	{% load my_filter %}
	{% for field in form %}
		<tr>
			<th class="chemprop">{{ field }} <span>{{ field.label }}</span></th>
			<td id="{{ field.id_for_label }}_ChemAxon" class="{{ field | property_availability:"chemaxon" }} chemaxon"></td>
			<td id="{{ field.id_for_label }}_EPI" class="{{ field | property_availability:"epi" }} epi"></td>
			<td id="{{ field.id_for_label }}_TEST" class="{{ field | property_availability:"test" }} test"></td>
			<td id="{{ field.id_for_label }}_SPARC" class="{{ field | property_availability:"sparc" }} sparc"></td>
		</tr>
	{% endfor %}
		<tr>
			<th></th>
			<td class="ChemCalcs_available">Available</td>
			<td class="ChemCalcs_unavailable">Unavailable</td>
		</tr>
	</table>
	"""
	return tmpl_ChemCalcsCTS

# def tmpl_TransformCTS():
# 	tmpl_TransformCTS = """
# 	<table class="input_table tab tab_Transform" style="display:none">
# 	{% for field in form %}
# 		<tr>
# 			<th>{{ field.label }}</th>
# 			<td>{{ field }}</td>
# 		</tr>
# 	{% endfor %}
# 	</table>
# 	"""
# 	return tmpl_TransformCTS

tmpl_ChemCalcsCTS = Template(tmpl_ChemCalcsCTS())
# tmpl_TransformCTS = Template(tmpl_TransformCTS())

# Method(s) called from *_inputs.py
def form():
	form_cts_ChemCalcs_props = cts_CemCalcs_props()
	html = tmpl_ChemCalcsCTS.render(Context(dict(form=form_cts_ChemCalcs_props)))
	# form_cts_Transform = cts_Transform()
	# html = html + tmpl_TransformCTS.render(Context(dict(form=form_cts_Transform)))
	return html

class cts_CemCalcs_props(forms.Form):
	melting_point = forms.BooleanField(required=False, label=mark_safe('Melting Point (&degC)'))
	boiling_point = forms.BooleanField(required=False, label=mark_safe('Boiling Point (&degC)'))
	water_sol = forms.BooleanField(required=False, label=mark_safe('Water Solubility'))
	vapor_press = forms.BooleanField(required=False, label=mark_safe('Vapor Pressure'))
	mol_diss = forms.BooleanField(required=False, label=mark_safe('Molecular Diffusivity (water)'))
	ionization_con = forms.BooleanField(required=False, label=mark_safe('Ionization Constant'))
	henrys_law_con = forms.BooleanField(required=False, label=mark_safe("Henry's Law Constant"))
	kow = forms.BooleanField(required=False, label=mark_safe('Octanol/Water Partition Coefficient'))
	koc = forms.BooleanField(required=False, label=mark_safe('Organic Carbon Partition Coefficient'))
	dist_coeff = forms.BooleanField(required=False, label=mark_safe('Distribution Coefficient'))







# class cts_Transform(forms.Form):
# 	reactionSys_CHOICES = (('Environmental', 'reactionSys_envir'),('Mammalian', 'reactionSys_mamm'))
# 	reactionSys = forms.ChoiceField(widget=forms.RadioSelect, choices=reactionSys_CHOICES, required=False, label='Reaction System')

# 	respiration_CHOICES = (('Aerobic', 'respiration_aerobic'),('Anaerobic', 'respiration_anaerobic'))
# 	respiration = forms.ChoiceField(widget=forms.RadioSelect, choices=respiration_CHOICES, required=False, label='Respiration')

	# reactionSys_CHOICES = (('', ''),('', ''),('', ''),('', ''))
	# aerobic_surfaceWater = 
	# aerobic_surfaceSoil = 
	# aerobic_vadose = 
	# aerobic_groundWater = 

	# reactionSys_CHOICES = (('', ''),('', ''),('', ''))
	# anaerobic_waterColumn = 
	# anaerobic_benthicSed = 
	# anaerobic_groundWater = 

	# reactionSys_CHOICES = (('', ''),('', ''),('', ''),('', ''),('', ''))
	# library_abioticHyd = 
	# library_aerobicBio = 
	# library_photolysis = 
	# library_abioticRed = 
	# library_anaerobicBio = 
	# library_mammalMeta = 