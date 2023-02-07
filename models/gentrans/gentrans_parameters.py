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
		{{form.respiration}}
	</td>

	{% endwith %}
	"""
	return tmpl_respirationTable

def tmpl_mammalian_choices():
	tmpl_mammalian_choices = """
	{% load filter_tags %}
	{% with form|get_class as name %}

	<td id="{{name}}">
		{{form.mammalian_choices}}
	</td>

	{% endwith %}
	"""
	return tmpl_mammalian_choices


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
			{% if field.label == "Biotransformer Mammalian Metabolism" %}
				<td>{{field}}</td>
				<td>
					{{field.label}}
					{{biotrans_libs.biotrans_libs}}
				</td>
			{% else %}
				<td>{{field}}</td>
				<td>{{field.label}}</td>
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
	<tr><th colspan="2">OCSPP Harmonized Guidelines</th></tr>
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
		{{form.ftt_selection}}
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
def form(formData, model='gentrans'):

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

	html += """<table id="mammalian_choices_tbl" class="input_table">
	<tr><th colspan="3"> Select a mammalian library </th></tr>
	<tr>
	"""
	form_cts_mammalian_choices = cts_mammalian_choices(formData)
	html += Template(tmpl_mammalian_choices()).render(Context(dict(form=form_cts_mammalian_choices, header=mark_safe("Mammalian Choices"))))
	html += '</tr></table>'

	# html = html + '<table id="cts_reaction_options" class="tbl_wrap"><tr><td>' # table wrapper for react libs and options 
	html += '<div id="alignLibAndOptions">'

	if model == 'biotrans':
		form_cts_reaction_libs = cts_biotrans_libs(formData)
	else:
		form_cts_reaction_libs = cts_reaction_libs(formData)
		form_cts_biotrans_libs = cts_biotrans_libs(formData)
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_reaction_libs, biotrans_libs=form_cts_biotrans_libs, header=mark_safe("Reaction Libraries"))))

	form_cts_class_specific_reaction_libs = cts_class_specific_reaction_libs(formData)
	html = html + tmpl_reactionSysCTS.render(Context(dict(form=form_cts_class_specific_reaction_libs, header=mark_safe("Chemical Class-Specific Reaction Libraries"))))	

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


reaction_pathway_CHOICES = (('0', 'Reaction System Guidelines'), ('1', 'OCSPP Harmonized Guidelines'), ('2', 'User selected (advanced)'))
reaction_sys_CHOICES = (('0', 'Environmental'), ('1', 'Mammalian'))
respiration_CHOICES = (('0', 'Make a selection'), ('1', 'Aerobic (abiotic)'), ('2', 'Aerobic (microbial)'), ('3', 'Anaerobic'))
mammalian_CHOICES = (('0', 'ChemAxon Metabolizer'), ('1', 'Biotransformer'))

# Reaction Options
gen_limit_CHOICES = (('1', 1), ('2', 2), ('3', 3), ('4', 4))  # generation limit
gen_limit_max = gen_limit_CHOICES[-1][1]  # not used as field, but referenced in many-a-place
pop_limit_CHOICES = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
					 ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'))  # population limit
tree_type_CHOICES = (('full_tree', 'Full tree'), ('simplified_tree', 'Simplified tree'))

# aerobic_CHOICES = (('0', 'Surface Water'), ('1', 'Surface Soil'), ('2', 'Vadose Zone'), ('3', 'Groundwater'))
# anaerobic_CHOICES = (('0', 'Water Column'), ('1', 'Benthic Sediment'), ('2', 'Groundwater'))

oecd_guidelines_CHOICES = (('0', 'Fate, Transport, and Transformation (Series 835)'), ('1', 'Metabolism and Pharmacokinetics (Series 870.7485)'))
ftt_CHOICES = (
	('0', 'Make a selection'),
	('1', 'Hydrolysis (835.2120 or 835.2240)'),
	('2', 'Direct Photolysis (835.2210 or 835.2240)'),
	('3', 'Aerobic Transformation (835.4100, 835.4300, 835.3180, 835.3190, 835.3280)'),
	('4', 'Anaerobic Transformation (835.4200, 835.4400, 835.3280, 835.5154)')
	# ('1', 'Laboratory Abiotic Transformation Guidelines'),
	# ('2', 'Transformation in Water and Soil Test Guidelines'),
	# ('3', 'Transformation Chemical-Specific Test Guidelines')
)
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


# Respiration
@parsleyfy
class cts_mammalian_choices(forms.Form):

	mammalian_choices = forms.ChoiceField(
				choices=mammalian_CHOICES,
				required=False)


@parsleyfy
class cts_biotrans_libs(forms.Form):
	biotrans_choices = (('cyp450', "Phase I (CYP450) Transformation"), ('ecbased', "EC-Based Transformation"),
		('phaseII', "PHASE II Transformation"), ('hgut', "Human Gut Microbial Transformation"))
	biotrans_libs = forms.ChoiceField(
					label='Biotransformer Choices',
					choices=biotrans_choices,
					widget=forms.Select(),
					required=False)


# Reaction Libraries
@parsleyfy
class cts_reaction_libs(forms.Form):
	abiotic_hydrolysis = forms.BooleanField(required=False, label='Abiotic Hydrolysis')
	abiotic_reduction = forms.BooleanField(required=False, label='Abiotic Reduction', disabled=True)
	photolysis_unranked = forms.BooleanField(required=False, label='Direct Photolysis (unranked)')  # unranked direct photolysis
	photolysis_ranked = forms.BooleanField(required=False, label='Direct Photolysis (ranked)')  # ranked direct photolysis
	aerobic_biodegrad = forms.BooleanField(required=False, label='Aerobic Biodegradation (under development)')
	anaerobic_biodegrad = forms.BooleanField(required=False, label='Anaerobic Biodegradation (under development)')
	mamm_metabolism = forms.BooleanField(required=False, label='Human Phase 1 Metabolism')
	biotrans_metabolism = forms.BooleanField(
		required=False,
		label='Biotransformer Mammalian Metabolism'
	)
	envipath_metabolism = forms.BooleanField(
		required=False,
		label='Envipath microbial biotransformation'
	)



@parsleyfy
class cts_class_specific_reaction_libs(forms.Form):
	# pfas_choices = (('pfas_environmental', "Experimentally verified transformations"),
	# 	('pfas_metabolism', "Proposed and expermentally verified transformations"))
	# pfas_environmental = forms.ChoiceField(
	# 	label='PFAS Environmental (under development)',
	# 	choices=pfas_choices,
	# 	widget=forms.Select(),
	# 	required=False,
	# 	disabled=True
	# )
	# pfas_metabolism = forms.ChoiceField(
	# 	label='PFAS Metabolism (under development)',
	# 	choices=pfas_choices,
	# 	widget=forms.Select(),
	# 	required=False,
	# 	disabled=True
	# )
	pfas_environmental = forms.BooleanField(required=False, label='PFAS Environmental', disabled=False)
	pfas_metabolism = forms.BooleanField(required=False, label='PFAS Metabolism', disabled=False)




# Reaction Options (e.g., generation limit, likely limit, etc.)
@parsleyfy
class cts_reaction_options(forms.Form):

	gen_limit = forms.ChoiceField (
					choices=gen_limit_CHOICES,
					label='Max number of generations',
					required=False,
					widget=forms.Select(attrs={'aria-label': 'select generation limit'})
				)

	tree_type = forms.ChoiceField (
					choices=tree_type_CHOICES,
					label='Select tree type',
					required=False,
					widget=forms.Select(attrs={'aria-label': 'select tree type'})
				)

	include_rates = forms.BooleanField(required=False, label='Include estimated transformation half-life (if available)', disabled=True)



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
					label="OCSPP Harmonized Guidelines",
					choices=oecd_guidelines_CHOICES,
					widget=forms.RadioSelect(),
					required=False)

	# Fate, Transport, and Transformation Selections:

	ftt_selection = forms.ChoiceField(
					choices=ftt_CHOICES,
					required=False,
					widget=forms.Select())
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


class GentransInp(cts_reaction_paths, cts_reaction_sys, cts_respiration, cts_mammalian_choices, cts_reaction_libs, cts_oecd_guidelines):
	pass


