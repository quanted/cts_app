# -*- coding: utf-8 -*-
"""
(np)
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
from parsley.decorators import parsleyfy
from django.template.loader import render_to_string


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

	{% endwith %}
	"""
	return tmpl_respirationTable


# Define Custom Templates
def tmpl_reactionSysCTS():
	tmpl_reactionSysCTS = """
	{% load filter_tags %}
	{% with form|get_class as name %}

	<table id={{name}} class="input_table">

	{% if name == "cts_reaction_paths" or name == "cts_reaction_sys" %}
		{% for field in form %}
			<tr><th colspan="{{field|length}}"> {{ field.label }}</th></tr>
			<tr>
			{% for item in field %}
				<td> {{ item }} </td>
			{% endfor %}
			</tr>
		{% endfor %}
	{% else %}
		<tr><th colspan="2"> {{header}} </th></tr>
		{% for field in form %}
			<tr>
			{% if field|is_checkbox %}
				<td>{{field}}</td>
				<td>{{field.label}}</td>
			{% else %}
				<td>{{field.label}}</td>
				<td>{{field}}</td>
			{% endif %}
			</tr>
		{% endfor %}
	{% endif %}

	{% endwith %}

	</table>
	"""
	return tmpl_reactionSysCTS


# Template for entire OECD Guidelines tree
def tmpl_oecdGuidelines():
	tmpl_oecdGuidelines = """
	{% load filter_tags %}

	<table id="oecd_selection" class="input_table">
	<tr><th colspan="2">OECD Selection</th></tr>
	<tr>
	{% for choice in form.oecd_selection %}
		<td> {{choice}} </td>
	{% endfor %}
	</tr>
	</table>

	<table id="ftt_selection" class="input_table">
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

	<table id="health_selection" class="input_table">
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


tmpl_reactionSysCTS = Template(tmpl_reactionSysCTS())
tmpl_respirationTable = Template(tmpl_respirationTable())
tmpl_oecdGuidelines = Template(tmpl_oecdGuidelines())


# Method(s) called from *_inputs.py
def form(formData):

	html = """
	<div class="input_table tab tab_ReactionPathSim" style="display:none">
	"""

	form_cts_reaction_paths = cts_reaction_paths(formData)	
	html += tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_paths)))

	form_oecd_guidelines = cts_oecd_guidelines(formData)
	html += tmpl_oecdGuidelines.render(Context(dict(form=form_oecd_guidelines)))

	form_cts_reaction_sys = cts_reaction_sys(formData)
	html += tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_sys, header=mark_safe("Reaction System"))))
	
	html += """<table id="respiration_tbl" class="input_table">
	<tr><th colspan="3"> Select a respiration type </th></tr>
	<tr>
	"""
	form_cts_respiration = cts_respiration(formData)
	html += tmpl_respirationTable.render(Context(dict(form=form_cts_respiration, header=mark_safe("Respiration"))))
	html += '</tr></table>'

	# html = html + '<table id="cts_reaction_options" class="tbl_wrap"><tr><td>' # table wrapper for react libs and options 
	html += '<div id="alignLibAndOptions">'

	form_cts_reaction_libs = cts_reaction_libs(formData)
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_libs, header=mark_safe("Reaction Libraries"))))

	# html = html + '</td><td>'

	form_cts_reaction_options = cts_reaction_options(formData)
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_options, header=mark_safe("Reaction Options"))))

	html += """
	</div>
	</div>
	"""

	# html = render_to_string('cts_gentrans_inputs.html', {
	# 							'reaction_paths': cts_reaction_paths(formData),
	# 							'reaction_sys': cts_reaction_sys(formData),
	# 							'respiration': cts_respiration(formData),
	# 							'reaction_libs': cts_reaction_libs(formData),
	# 							'reaction_options': cts_reaction_options(formData)
	# 						})

	return html


reaction_pathway_CHOICES = (('0', 'Reaction System Guidelines'), ('1', 'OCSPP Guidelines'), ('2', 'User selected (advanced)'))
reaction_sys_CHOICES = (('0', 'Environmental'), ('1', 'Mammalian'))
respiration_CHOICES = (('0', 'Make a selection'), ('1', 'Aerobic'), ('2', 'Anaerobic'))

# Reaction Options
gen_limit_CHOICES = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'))  # generation limit
gen_limit_max = gen_limit_CHOICES[-1][1]  # not used as field, but referenced in many-a-place
pop_limit_CHOICES = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                     ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'))  # population limit

# aerobic_CHOICES = (('0', 'Surface Water'), ('1', 'Surface Soil'), ('2', 'Vadose Zone'), ('3', 'Groundwater'))
# anaerobic_CHOICES = (('0', 'Water Column'), ('1', 'Benthic Sediment'), ('2', 'Groundwater'))

oecd_guidelines_CHOICES = (('0', 'Fate, Transport, and Transformation (Series 835)'), ('1', 'Health Effects (Series 870)'))
ftt_CHOICES = (('0', 'Make a selection'), ('1', 'Laboratory Abiotic Transformation Guidelines'), ('2', 'Transformation in Water and Soil Test Guidelines'), ('3', 'Transformation Chemical-Specific Test Guidelines'))
labAbioTrans_CHOICES = (('0', 'Abiotic Hydrolysis (835.2120)'), ('1', 'Abiotic Reduction (no available guideline)'), ('2', 'Photolysis in Water (currently under development) (835.22440)'))
transWaterSoil_CHOICES = (('0', 'Aerobic Soil Biodegradation (835.4100)'), ('1', 'Anaerobic Soil Biodegradation (currently under development) (835.4200)'))
transChemSpec_CHOICES = [('0', 'Anaerobic Biodegradation in the Subsurface (currently under development) (835.5154)')]
specialStudies_CHOICES = [('0', 'Metabolism and Pharmacokinetics (870.7485)')]


# Reaction Pathways
@parsleyfy
class cts_reaction_paths(forms.Form):

	reaction_paths = forms.ChoiceField(
					# label='Reaction Paths',
					label='Options for selecting Reaction Libraries',
					choices=reaction_pathway_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

# Reaction System
@parsleyfy
class cts_reaction_sys(forms.Form):

	reaction_system = forms.ChoiceField(
					choices=reaction_sys_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

# Respiration
@parsleyfy
class cts_respiration(forms.Form):

	respiration = forms.ChoiceField(
				choices=respiration_CHOICES,
				required=False)

	# aerobic = forms.ChoiceField(
	# 			choices=aerobic_CHOICES,
	# 			widget=forms.RadioSelect(),
	# 			required=False)

	# anaerobic = forms.ChoiceField(
	# 			choices=anaerobic_CHOICES,
	# 			widget=forms.RadioSelect(),
	# 			required=False)


# Reaction Libraries
@parsleyfy
class cts_reaction_libs(forms.Form):
	abiotic_hydrolysis = forms.BooleanField(required=False, label='Abiotic Hydrolysis')
	aerobic_biodegrad = forms.BooleanField(required=False, label='Aerobic Biodegradation')
	photolysis = forms.BooleanField(required=False, label='Photolysis')
	abiotic_reduction = forms.BooleanField(required=False, label='Abiotic Reduction')
	anaerobic_biodegrad = forms.BooleanField(required=False, label='Anaerobic Biodegradation')
	mamm_metabolism = forms.BooleanField(required=False, label='Mammalian Metabolism')


# Reaction Options (e.g., generation limit, likely limit, etc.)
@parsleyfy
class cts_reaction_options(forms.Form):

	gen_limit = forms.ChoiceField (
					choices=gen_limit_CHOICES,
					label='Max number of generations:',
					required=False
				)	

	# pop_limit = forms.ChoiceField (
	# 				choices=pop_limit_CHOICES,
	# 				label='Population Limit:',
	# 				required=False,
	# 			)

	# likely_limit = forms.FloatField (
	# 					label='Likelihood limit:',
	# 					initial=0.001,
	# 					min_value=0.001,
	# 					max_value=0.99,
	# 				)

	# add clean to force select option range
    # def clean_status(self):
    #    return self.instance.status


# OECD Guidelines Selection
@parsleyfy
class cts_oecd_guidelines(forms.Form):

	# Main Selection Branch
	oecd_selection = forms.ChoiceField(
					label="OECD Selection",
					choices=oecd_guidelines_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

	# Fate, Transport, and Transformation Selections:

	ftt_selection = forms.ChoiceField(
					choices=ftt_CHOICES)
					# widget=forms.RadioSelect())

	labAbioTrans_selection = forms.ChoiceField(
					choices=labAbioTrans_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

	transWaterSoil_selection = forms.ChoiceField(
					choices=transWaterSoil_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

	transChemSpec_selection = forms.ChoiceField(
					choices=transChemSpec_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

	# Health Effects Selections:
	specialStudies_selection = forms.ChoiceField(
					choices=specialStudies_CHOICES,
					widget=forms.RadioSelect(),
					required=False)


class GentransInp(cts_reaction_paths, cts_reaction_sys, cts_respiration, cts_reaction_libs, cts_oecd_guidelines):
	pass


