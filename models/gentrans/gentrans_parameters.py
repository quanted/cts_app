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
def tmpl_reactionSysCTS():
	tmpl_reactionSysCTS = """
	{% load class_tag %}
	{% with form|get_class as name%}
	<table id="{{name}}">
	<tr><th colspan="2" class="ctsInputHeader">{{ header }}</th></tr>
	{% if name == "cts_path_sim" %}
		{% for choice in form.reaction_paths %}
			<tr><td>{{ choice }}</td></tr>
		{% endfor %}
	{% endif %}
	{% if name == "cts_respiration" %}
		{% for choice in form.respiration %}
			<tr><td>{{ choice }}</td></tr>
		{% endfor %}
	{% endif %}
	{% if name == "cts_react_sys" %}
		{% for choice in form.reaction_system %}
			<tr><td>{{ choice }}</td></tr>
		{% endfor %}
	{% endif %}
	{% if name == "cts_aerobic" or name == "cts_anaerobic" or name == "cts_reaction_libs" %}
		{% for field in form %}
			{% if field|is_checkbox %}
				<tr><td>{{ field }} {{ field.label }}</td></tr>
			{% else %}
				<tr><td>{{ field.label_tag }} {{ field }}</td></tr>
 			{% endif %}
		{% endfor %}
	{% endif %}
	</table>
	{%endwith%}
	"""
	return tmpl_reactionSysCTS

tmpl_reactionSysCTS = Template(tmpl_reactionSysCTS())

# Method(s) called from *_inputs.py
def form():
	html = '<div class="input_table tab tab_ReactionPathSim" style="display:none">'

	form_cts_path_sim = cts_path_sim()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_path_sim, header=mark_safe("Reaction Pathway Simulator"))))

	form_cts_react_sys = cts_react_sys()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_react_sys, header=mark_safe("Reaction System"))))
	
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



reaction_pathway_CHOICES = (('0', 'Reaction System'), ('1', 'OECD Guidelines'), ('2', 'Reaction Library'))
reaction_sys_CHOICES = (('0', 'Environmental'), ('1', 'Mammalian'))
respiration_CHOICES = (('0', 'Aerobic'), ('1', 'Anaerobic'))

# Reaction Pathway Simulator
class cts_path_sim(forms.Form):
	reaction_paths = forms.ChoiceField(
					# required=True,
					# label='Reaction Systems',
					choices=reaction_pathway_CHOICES,
					# validators=[validation.validate_choicefield],
					widget=forms.RadioSelect())

# Reaction Systems
class cts_react_sys(forms.Form):
	reaction_system = forms.ChoiceField(
					# required=True,
					# label='Reaction Systems',
					choices=reaction_sys_CHOICES,
					# validators=[validation.validate_choicefield],
					widget=forms.RadioSelect())

# Respiration
class cts_respiration(forms.Form):
	respiration = forms.ChoiceField(required=True,
				# label='',
				choices=respiration_CHOICES,
				# initial='Make a selection',
				# validators=[validation.validate_choicefield])
				widget=forms.RadioSelect())

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
