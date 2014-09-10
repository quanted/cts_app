# -*- coding: utf-8 -*-
"""
nickp
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
from models.forms import validation

# tmpl_reactionSysCTS = """
# 	{% load class_tag %}
# 	<table class="input_table tab tab_{{form|get_class}}" style="display:none">
# 		<tr><th colspan="2" class="ctsInputHeader">{{ header }}</th></tr>
# 	{% for field in form %}
# 		<tr><th>{{ field.label_tag }}</th><td>{{ field }}</td></tr>
# 	{% endfor %}
# 	</table>
	# """

	# <th>{{ field }} <span>{{ field.label }}</span></th>
	# <td id="{{ ChoiceFieldld.id_for_label }}_ChemAxon" class="{{ field | property_availability:"chemaxon" }}"></td>
# <tr><td id="align_cell">{{ field }}<span>{{ field.label }}</span></td></tr>
# Define Custom Templates
def tmpl_reactionSysCTS():
	tmpl_reactionSysCTS = """
	{% load class_tag %}
	<table class="no_border" id="{{form|get_class}}">
	<tr><th colspan="2" class="ctsInputHeader">{{ header }}</th></tr>
	{% for field in form %}
		{% if field|is_checkbox %}
			<tr><td>{{ field }} {{ field.label }}</td></tr>
		{% else %}
			<tr><td>{{ field.label_tag }} {{ field }}</td></tr>
		{% endif %}
	{% endfor %}
	</table>
	"""
	return tmpl_reactionSysCTS

tmpl_reactionSysCTS = Template(tmpl_reactionSysCTS())

# Method(s) called from *_inputs.py
def form():
	html = '<div class="input_table tab tab_ReactionPathSim" style="display:none">'

	form_cts_reaction_sys = cts_reaction_sys()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_sys, header=mark_safe("Reaction Pathway Simulator"))))
	
	form_cts_respiration = cts_respiration()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_respiration, header=mark_safe("Respiration"))))

	form_cts_aerobic = cts_aerobic()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_aerobic, header=mark_safe("Aerobic"))))

	form_cts_anaerobic = cts_anaerobic()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_anaerobic, header=mark_safe("Anaerobic"))))

	form_cts_reaction_libs = cts_reaction_libs()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_libs, header=mark_safe("Reaction Libraries"))))

	html = html + '</div>'

	return html



reaction_sys_CHOICES = (('0', 'Make a selection'), ('1', 'Environmental'), ('2', 'Mammalian'))
respiration_CHOICES = (('0', 'Make a selection'), ('1', 'Aerobic'), ('2', 'Anaerobic'))

# Reaction Pathway Simulator
class cts_reaction_sys(forms.Form):
	reaction_systems = forms.ChoiceField(required=True,
					label='Reaction System',
					choices=reaction_sys_CHOICES,
					initial='Make a selection',
					validators=[validation.validate_choicefield])

# Respiration
class cts_respiration(forms.Form):
	respiration = forms.ChoiceField(required=True,
				label='',
				choices=respiration_CHOICES,
				initial='Make a selection',
				validators=[validation.validate_choicefield])

# Aerobic 
class cts_aerobic(forms.Form):
	surface_water = forms.BooleanField(required=False, label='Surface Water')
	surface_soil = forms.BooleanField(required=False, label='Surface Soil')
	vadose_zone = forms.BooleanField(required=False, label='Vadose Zone')
	aGroundwater = forms.BooleanField(required=False, label='Groundwater')

# Anaerobic 
class cts_anaerobic(forms.Form):
	water_col = forms.BooleanField(required=False, label='Water Column')
	benthic_sediment = forms.BooleanField(required=False, label='Benthic Sediment')
	anGroundwater = forms.BooleanField(required=False, label='Anaerobic Groundwater')

# Reaction Libraries
class cts_reaction_libs(forms.Form):
	abiotic_hydrolysis = forms.BooleanField(required=False, label='Abiotic Hydrolysis')
	aerobic_biodegrad = forms.BooleanField(required=False, label='Aerobic Biodegradation')
	photolysis = forms.BooleanField(required=False, label='Photolysis')
	abiotic_reduction = forms.BooleanField(required=False, label='Abiotic Reduction')
	anaerobic_biodegrad = forms.BooleanField(required=False, label='Anaerobic Biodegradation')
	mamm_metabolism = forms.BooleanField(required=False, label='Mammalian Metabolism')
