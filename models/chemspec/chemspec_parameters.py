# -*- coding: utf-8 -*-
"""
@author: np
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
from django.core import validators
from models.forms import validation
import logging


def tmpl_chemstructCTS():
	tmpl_chemstructCTS = """
		<div id="chemEditLookup">
		<table class="input_table tab tab_Chemical">
			<tr>
				<td colspan="2"><span>{{ header }}</span>
				<input id="setSmilesButton" class="tab_chemicalButtons" type="button" value="Enter a SMILES, IUPAC or CAS# and click here">
				<br>{{form.field.errors}}</td>
			</tr>
		{% for field in form %}
			<tr><td>{{field}}</td></tr>
		{% endfor %}
		</table>
		</div>
		"""
	return tmpl_chemstructCTS


# Define Custom Templates
def tmpl_speciationCTS():
	tmpl_speciationCTS = """
	{% load filter_tags %}
	{% with form|get_class as name %}

	<table class="input_table tab tab_Speciation" name="{{name}}" style="display:none">

	{% if name == "CTS_Speciation_Pka" %}
		<tr><th colspan="2" class="ctsInputHeader">{{ form.pka_chkbox }} {{ header }}</th></tr>
	{% elif name == "CTS_Speciation_Tautomer" %}
		<tr><th colspan="2" class="ctsInputHeader">{{ form.tautomer_chkbox }} {{ header }}</th></tr>
	{% elif name == "CTS_Speciation_Stereoisomers" %}
		<tr><th colspan="2" class="ctsInputHeader">{{ form.stereoisomer_chkbox }} {{ header }}</th></tr>
	{% endif %}
		
	{% for field in form %}
		{% if not field|is_checkbox %}
			<tr><th>{{ field.label_tag }}</th><td>{{ field }}<br>{{ field.errors }}</td></tr>
		{% endif %}
	{% endfor %}

	{% endwith %}
	</table>
	"""
	return tmpl_speciationCTS

tmpl_speciationCTS = Template(tmpl_speciationCTS())
tmpl_chemstructCTS = Template(tmpl_chemstructCTS())

# Method(s) called from *_inputs.py
def form(formData):
	form_cts_chemical_structure = CTS_Chemical_Structure(formData)
	html = tmpl_chemstructCTS.render(Context(dict(form=form_cts_chemical_structure, header=mark_safe("Lookup Chemical")))) 
	form_cts_speciation_pKa = CTS_Speciation_Pka(formData)
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_pKa, header=mark_safe("Calculate Ionization Constants (p<i>K</i>a) Parameters"))))
	form_cts_speciation_tautomer = CTS_Speciation_Tautomer(formData)
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_tautomer, header="Calculate Dominant Tautomer Distribution")))
	form_cts_speciation_stereoisomers = CTS_Speciation_Stereoisomers(formData)
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_stereoisomers, header="Calculate Stereoisomers")))
	return html


"""Chemical Editor"""
class CTS_Chemical_Structure(forms.Form):

	chem_struct = forms.CharField (
					widget=forms.Textarea(attrs={'cols':50, 'rows':2}),
					initial='',
					label='Chemical Structure',
					required=True,
					# validators=[]
				)


"""Chemical Speciation"""

# pka table
class CTS_Speciation_Pka(forms.Form):


	pKa_decimals = forms.FloatField (
						label='Number of Decimals', 
						initial='2', 
						required=True,
						validators=[validation.validate_greaterthan0]
					)

	pKa_pH_lower = forms.FloatField (
						label='pH Lower Limit',
						initial='0',
						required=False,
						validators=[validation.validate_number]
					)

	pKa_pH_upper = forms.FloatField (
						label='pH Upper Limit',
						initial='14',
						required=False
					)

	pKa_pH_increment = forms.FloatField (
						label='pH Step Size',
						initial='0.2',
						validators=[validation.validate_greaterthan0, validators.MaxValueValidator(14)],
						required=False
					)

	pH_microspecies = forms.FloatField (
						label='Generate Major Microspeices at pH',
						initial='7.0',
						required=False
					)

	isoelectricPoint_pH_increment = forms.FloatField (
						label=mark_safe('Isoelectric Point (pl) <br> pH Step Size for Charge Distribution'),
						initial='0.5',
						required=False
					)

	# Check box for selecting table
	pka_chkbox = forms.BooleanField (
						label='',
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False
					)


# tautomerization table
class CTS_Speciation_Tautomer(forms.Form):

	tautomer_maxNoOfStructures = forms.FloatField (
						label='Maximum Number of Structures', 
						initial='100',
						required=False
					)

	tautomer_pH = forms.FloatField (
						label='at pH',
						initial='7.0',
						required=False
					)

	tautomer_chkbox = forms.BooleanField (
						label='', 
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False
					)


# stereoisomer table
class CTS_Speciation_Stereoisomers(forms.Form):

	stereoisomers_maxNoOfStructures = forms.FloatField (
						label='Maximum Number of Structures',
						initial='100',
						required=False
					)

	stereoisomer_chkbox = forms.BooleanField (
						label='', 
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False
					)

class ChemspecInp(CTS_Chemical_Structure, CTS_Speciation_Pka, CTS_Speciation_Tautomer, CTS_Speciation_Stereoisomers):
	pass