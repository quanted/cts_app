# -*- coding: utf-8 -*-
"""
nickp
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
from models.forms import validation

# Old template for dropboxes:
# {% load class_tag %}
# 	<table class="no_border" id="{{form|get_class}}">
# 	<tr><th colspan="2" class="ctsInputHeader">{{ header }}</th></tr>
# 	{% for field in form %}
# 		{% if field|is_checkbox %}
# 			<tr><td>{{ field }} {{ field.label }}</td></tr>
# 		{% else %}
# 			<tr><td>{{ field.label_tag }} {{ field }}</td></tr>
# 		{% endif %}
# 	{% endfor %}
# 	</table>


# Define Custom Templates
# def tmpl_reactionSysCTS():
# 	tmpl_reactionSysCTS = """
# 	{% load class_tag %}
# 	{% with form|get_class as name%}
# 	<table id="{{name}}">
# 	<tr><th colspan="2" class="ctsInputHeader">{{ header }}</th></tr>
# 	{% if name == "cts_path_sim" %}
# 		{% for choice in form.reaction_paths %}
# 			<tr><td>{{ choice }}</td></tr>
# 		{% endfor %}
# 	{% endif %}
# 	{% if name == "cts_respiration" %}
# 		{% for choice in form.respiration %}
# 			<tr><td>{{ choice }}</td></tr>
# 		{% endfor %}
# 	{% endif %}
# 	{% if name == "cts_react_sys" %}
# 		{% for choice in form.reaction_system %}
# 			<tr><td>{{ choice }}</td></tr>
# 		{% endfor %}
# 	{% endif %}
# 	{% if name == "cts_aerobic" or name == "cts_anaerobic" or name == "cts_reaction_libs" %}
# 		{% for field in form %}
# 			{% if field|is_checkbox %}
# 				<tr><td>{{ field }} {{ field.label }}</td></tr>
# 			{% else %}
# 				<tr><td>{{ field.label_tag }} {{ field }}</td></tr>
#  			{% endif %}
# 		{% endfor %}
# 	{% endif %}
# 	</table>
# 	{%endwith%}
# 	"""
# 	return tmpl_reactionSysCTS

def tmpl_reactionSysCTS():
	tmpl_reactionSysCTS = """
	{% load class_tag %}
	{% with form|get_class as name %}
	{% if name == "cts_path_sim_1" %}
		{% for choice in form %}
			<tr><td> {{ choice }} </td></tr>
		{%endfor%}
	{% else %}
		{% for field in form %}
			<tr><td> {{ field.label }} </td></tr>
			{% if field|is_checkbox %}
 				<tr><td>{{ field }} {{ field.label }}</td></tr>
 			{% else %}
 				<tr><td>{{ field.label_tag }} {{ field }}</td></tr>
  			{% endif %}
		{%endfor%}
	{% endif %}
	{% endwith %}
	"""
	return tmpl_reactionSysCTS

tmpl_reactionSysCTS = Template(tmpl_reactionSysCTS())

# Method(s) called from *_inputs.py
def form():

	# html = '<div class="input_table tab tab_ReactionPathSim" style="display:none">'

	html = '<table id="cts_path_sim">'

	form_cts_path_sim_1 = cts_path_sim_1()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_path_sim_1)))

	form_cts_path_sim_2 = cts_path_sim_2()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_path_sim_2)))

	form_cts_path_sim_3 = cts_path_sim_3()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_path_sim_3)))

	form_cts_path_sim_4 = cts_path_sim_4()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_path_sim_4)))

	html = html + '</table>'

	return html



reaction_pathway_CHOICES = (('0', 'Reaction System'), ('1', 'OECD Guidelines'), ('2', 'Reaction Library'))
reaction_sys_CHOICES = (('0', 'Environmental'), ('1', 'Mammalian'))
respiration_CHOICES = (('0', 'Aerobic'), ('1', 'Anaerobic'))

# Reaction Pathway Simulator
class cts_path_sim_1(forms.Form):

	# Reaction Paths
	reaction_paths = forms.ChoiceField(
					# required=True,
					label='Reaction Paths',
					choices=reaction_pathway_CHOICES,
					# validators=[validation.validate_choicefield],
					widget=forms.RadioSelect())

	# Reaction System
	reaction_system = forms.ChoiceField(
					# required=True,
					# label='Reaction Systems',
					choices=reaction_sys_CHOICES,
					# validators=[validation.validate_choicefield],
					widget=forms.RadioSelect())


	# Respiration
	respiration = forms.ChoiceField(required=True,
				# label='',
				choices=respiration_CHOICES,
				# initial='Make a selection',
				# validators=[validation.validate_choicefield])
				widget=forms.RadioSelect())

class cts_path_sim_2(forms.Form):

	# Aerobic
	surface_water = forms.BooleanField(required=False, label='Surface Water')
	surface_soil = forms.BooleanField(required=False, label='Surface Soil')
	vadose_zone = forms.BooleanField(required=False, label='Vadose Zone')
	aGroundwater = forms.BooleanField(required=False, label='Groundwater')

class cts_path_sim_3(forms.Form):

	# Anaerobic
	water_col = forms.BooleanField(required=False, label='Water Column')
	benthic_sediment = forms.BooleanField(required=False, label='Benthic Sediment')
	anGroundwater = forms.BooleanField(required=False, label='Anaerobic Groundwater')

class cts_path_sim_4(forms.Form):

	# Reaction Libraries
	abiotic_hydrolysis = forms.BooleanField(required=False, label='Abiotic Hydrolysis')
	aerobic_biodegrad = forms.BooleanField(required=False, label='Aerobic Biodegradation')
	photolysis = forms.BooleanField(required=False, label='Photolysis')
	abiotic_reduction = forms.BooleanField(required=False, label='Abiotic Reduction')
	anaerobic_biodegrad = forms.BooleanField(required=False, label='Anaerobic Biodegradation')
	mamm_metabolism = forms.BooleanField(required=False, label='Mammalian Metabolism')
