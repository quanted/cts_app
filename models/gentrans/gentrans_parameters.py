# -*- coding: utf-8 -*-
"""
nickp
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
from models.forms import validation


# Horizontally-aligned radio buttons template
def tmpl_respirationTable():
	tmpl_respirationTable = """
	{% load filter_tags %}
	{% with form|get_class as name %}

	<td id="{{name}}">
	{% for choice in form.respiration %}
		{{ choice }} <br>
	{% endfor %}
	</td>

	<td id="aerobic_picks">
	<b>Aerobic</b> <br>
	{%for choice in form.aerobic %}
		{{choice}} <br>
	{% endfor %}
	</td>

	<td id="anaerobic_picks">
	<b>Anaerobic</b> <br>
	{%for choice in form.anaerobic %}
		{{choice}} <br>
	{% endfor %}
	</td>

	{% endwith %}
	"""
	return tmpl_respirationTable


# Define Custom Templates
def tmpl_reactionSysCTS():
	tmpl_reactionSysCTS = """
	{% load filter_tags %}
	{% with form|get_class as name %}

	<table id={{name}}>

	{% if name == "cts_reaction_paths" or name == "cts_reaction_sys" %}
		{% for field in form %}
			<tr><th colspan="{{field|length}}"> {{ field.label }}</th></tr>
			<tr>
			{% for item in field %}
				<td> {{ item }} </td>
			{% endfor %}
			</tr>
		{% endfor %}
	{% elif name == "cts_reaction_libs" %}
		<tr><th> Reaction Libraries </th></tr>
		<tr><td>
		{% for field in form %}
			{{field}} {{field.label}} <br>
		{% endfor %}
		</tr></td>
	{% endif %}

	{% endwith %}

	</table>
	"""
	return tmpl_reactionSysCTS


# Template for entire OECD Guidelines tree
def tmpl_oecdGuidelines():
	tmpl_oecdGuidelines = """
	{% load filter_tags %}

	<table id="oecd_selection">
	<tr><th colspan="2">OECD Selection</th></tr>
	<tr>
	{% for choice in form.oecd_selection %}
		<td> {{choice}} </td>
	{% endfor %}
	</tr>
	</table>

	<table id="ftt_selection">
	<tr><th colspan="4">Fate, Transport, and Transformation</th></tr>
	<tr>
	<td>
	{% for choice in form.ftt_selection %}
		{{ choice }} <br>
	{% endfor %}
	</td>
	<td id="labAbioTrans_picks">
	{% for choice in form.labAbioTrans_selection %}
		{{ choice }} <br>
	{% endfor %}
	</td>
	<td id="transWaterSoil_picks">
	{% for choice in form.transWaterSoil_selection %}
		{{ choice }} <br>
	{% endfor %}
	</td>
	<td id="transChemSpec_picks">
	{% for choice in form.transChemSpec_selection %}
		{{ choice }} <br>
	{% endfor %}
	</td>
	</tr>
	</table>

	<table id="health_selection">
	<tr><th colspan="2">Health Effects</th></tr>
	<tr>
	<td>Special Studies Test Guidelines: </td>
	<td>
	{% for choice in form.specialStudies_selection %}
		{{ choice }} <br>
	{% endfor %}
	</td>
	</tr>
	</table>
	"""
	return tmpl_oecdGuidelines


# tmpl_horizontalRadios = Template(tmpl_horizontalRadios())
tmpl_reactionSysCTS = Template(tmpl_reactionSysCTS())
tmpl_respirationTable = Template(tmpl_respirationTable())
tmpl_oecdGuidelines = Template(tmpl_oecdGuidelines())

# Method(s) called from *_inputs.py
def form():

	html = '<div class="input_table tab tab_ReactionPathSim" style="display:none">'

	form_cts_reaction_paths= cts_reaction_paths()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_paths)))

	form_oecd_guidelines= cts_oecd_guidelines()
	html = html + tmpl_oecdGuidelines.render(Context(dict(form=form_oecd_guidelines)))

	form_cts_reaction_sys = cts_reaction_sys()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_sys, header=mark_safe("Reaction System"))))
	
	html = html + """<table id="respiration_tbl">
	<tr><th colspan="3"> Select a respiration type </th></tr>
	<tr>
	"""

	form_cts_respiration = cts_respiration()
	html = html + tmpl_respirationTable.render(Context(dict(form=form_cts_respiration, header=mark_safe("Respiration"))))

	# form_cts_aerobic = cts_aerobic()
	# html = html + tmpl_respirationTable.render(Context(dict(form=form_cts_aerobic, header=mark_safe("Aerobic"))))

	# form_cts_anaerobic = cts_anaerobic()
	# html = html + tmpl_respirationTable.render(Context(dict(form=form_cts_anaerobic, header=mark_safe("Anaerobic"))))

	html = html + '</tr></table>'

	form_cts_reaction_libs = cts_reaction_libs()
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_libs, header=mark_safe("Reaction Libraries"))))

	html = html + '</div>'

	return html


reaction_pathway_CHOICES = (('0', 'Reaction System'), ('1', 'OECD Guidelines'), ('2', 'Reaction Library'))
reaction_sys_CHOICES = (('0', 'Environmental'), ('1', 'Mammalian'))
respiration_CHOICES = (('0', 'Aerobic'), ('1', 'Anaerobic'))

aerobic_CHOICES = (('0', 'Surface Water'), ('1', 'Surface Soil'), ('2', 'Vadose Zone'), ('3', 'Groundwater'))
anaerobic_CHOICES = (('0', 'Water Column'), ('1', 'Benthic Sediment'), ('2', 'Groundwater'))

oecd_guidelines_CHOICES = (('0', 'Fate, Transport, and Transformation (Series 835)'), ('1', 'Health Effects (Series 870)'))
ftt_CHOICES = (('0', 'Laboratory Abiotic Transformation Guidelines'), ('1', 'Transformation in Water and Soil Test Guidelines'), ('2', 'Transformation Chemical-Specific Test Guidelines'))
labAbioTrans_CHOICES = (('0', 'Abiotic Hydrolysis (835.2120)'), ('1', 'Abiotic Reduction (no available guideline)'), ('2', 'Photolysis in Water (currently under development) (835.22440)'))
transWaterSoil_CHOICES = (('0', 'Aerobic Soil Biodegradation (835.4100)'), ('1', 'Anaerobic Soil Biodegradation (currently under development) (835.4200)'))
transChemSpec_CHOICES = [('0', 'Anaerobic Biodegradation in the Subsurface (currently under development) (835.5154)')]
specialStudies_CHOICES = [('0', 'Metabolism and Pharmacokinetics (870.7485)')]


# Reaction Pathways
class cts_reaction_paths(forms.Form):

	reaction_paths = forms.ChoiceField(
					label='Reaction Paths',
					choices=reaction_pathway_CHOICES,
					widget=forms.RadioSelect())

# Reaction System
class cts_reaction_sys(forms.Form):

	reaction_system = forms.ChoiceField(
					choices=reaction_sys_CHOICES,
					widget=forms.RadioSelect())

# Respiration
class cts_respiration(forms.Form):

	respiration = forms.ChoiceField(
				choices=respiration_CHOICES,
				widget=forms.RadioSelect())

	aerobic = forms.ChoiceField(
				choices=aerobic_CHOICES,
				widget=forms.RadioSelect())

	anaerobic = forms.ChoiceField(
				choices=anaerobic_CHOICES,
				widget=forms.RadioSelect())

# Aerobic 
# class cts_aerobic(forms.Form):

# 	surface_water = forms.BooleanField(required=False, label='Surface Water')
# 	surface_soil = forms.BooleanField(required=False, label='Surface Soil')
# 	vadose_zone = forms.BooleanField(required=False, label='Vadose Zone')
# 	aGroundwater = forms.BooleanField(required=False, label='Groundwater')

# Anaerobic 
# class cts_anaerobic(forms.Form):
# 	water_col = forms.BooleanField(required=False, label='Water Column')
# 	benthic_sediment = forms.BooleanField(required=False, label='Benthic Sediment')
# 	anGroundwater = forms.BooleanField(required=False, label='Anaerobic Groundwater')

# Reaction Libraries
class cts_reaction_libs(forms.Form):
	abiotic_hydrolysis = forms.BooleanField(required=False, label='Abiotic Hydrolysis')
	aerobic_biodegrad = forms.BooleanField(required=False, label='Aerobic Biodegradation')
	photolysis = forms.BooleanField(required=False, label='Photolysis')
	abiotic_reduction = forms.BooleanField(required=False, label='Abiotic Reduction')
	anaerobic_biodegrad = forms.BooleanField(required=False, label='Anaerobic Biodegradation')
	mamm_metabolism = forms.BooleanField(required=False, label='Mammalian Metabolism')

# OECD Guidelines Selection
class cts_oecd_guidelines(forms.Form):

	# Main Selection Branch
	oecd_selection = forms.ChoiceField(
					label="OECD Selection",
					choices=oecd_guidelines_CHOICES,
					widget=forms.RadioSelect())

	# Fate, Transport, and Transformation Selections:

	ftt_selection = forms.ChoiceField(
					choices=ftt_CHOICES,
					widget=forms.RadioSelect())

	labAbioTrans_selection = forms.ChoiceField(
					choices=labAbioTrans_CHOICES,
					widget=forms.RadioSelect())

	transWaterSoil_selection = forms.ChoiceField(
					choices=transWaterSoil_CHOICES,
					widget=forms.RadioSelect())

	transChemSpec_selection = forms.ChoiceField(
					choices=transChemSpec_CHOICES,
					widget=forms.RadioSelect())

	# Health Effects Selections:

	specialStudies_selection = forms.ChoiceField(
					choices=specialStudies_CHOICES,
					widget=forms.RadioSelect())



