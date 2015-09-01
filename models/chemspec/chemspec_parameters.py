# -*- coding: utf-8 -*-
"""
@author: np
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
from models.forms import validation
import logging
from parsley.decorators import parsleyfy


def tmpl_chemstructCTS():
	tmpl_chemstructCTS = """
		<div id="chemEditLookup">
		<table class="input_table tab tab_Chemical">
			<tr>
				<td colspan="2"><span>{{ header }}</span>
				<input id="setSmilesButton" class="tab_chemicalButtons" type="button" value="Enter a SMILES, IUPAC or CAS# and Click Here">
				</td>
			</tr>
		{% for field in form %}
			<tr><td>{{field}}<br>{{field.errors}}</td></tr>
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
	html += tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_pKa, header=mark_safe("Calculate Ionization Constants (p<i>K</i>a) Parameters"))))
	form_cts_speciation_tautomer = CTS_Speciation_Tautomer(formData)
	html += tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_tautomer, header="Calculate Dominant Tautomer Distribution")))
	form_cts_speciation_stereoisomers = CTS_Speciation_Stereoisomers(formData)
	html += tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_stereoisomers, header="Calculate Stereoisomers")))
	return html


@parsleyfy
class CTS_Chemical_Structure(forms.Form):
	"""
	Chemical Editor
	"""

	chem_struct = forms.CharField (
					widget=forms.Textarea(attrs={'cols':50, 'rows':2}),
					initial='',
					label='Chemical Structure',
				)


@parsleyfy
class CTS_Speciation_Pka(forms.Form):
	"""
	Chemical Speciation
	"""

	pKa_decimals = forms.FloatField (
						label='Number of Decimals', 
						initial=3,
						min_value=1,
						max_value=10,
						# required=False,
					)

	pKa_pH_lower = forms.FloatField (
						label='pH Lower Limit',
						initial=0,
						min_value=0,
						max_value=14,
						# required=False,
					)

	pKa_pH_upper = forms.FloatField (
						label='pH Upper Limit',
						initial=14,
						min_value=0,
						max_value=14,
						# required=False,
					)

	pKa_pH_increment = forms.FloatField (
						label='pH Step Size',
						initial=0.2,
						min_value=0.1,
						max_value=1.0,
						# required=False,
					)

	pH_microspecies = forms.FloatField (
						label='Generate Major Microspecies at pH',
						initial=7.0,
						min_value=0,
						max_value=14,
						# required=False,
					)

	isoelectricPoint_pH_increment = forms.FloatField (
						label=mark_safe('Isoelectric Point (pl) <br> pH Step Size for Charge Distribution'),
						initial=0.5,
						min_value=0.1,
						max_value=1.0,
						# required=False,
					)

	# Check box for selecting table
	pka_chkbox = forms.BooleanField (
						label='',
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False,
					)


	def clean(self):
		"""
		Function for individually-validated fields;
		used for field-dependant conditionals 
		"""

		# +++ Django 1.8 Way +++
		# cleanedData = super(CTS_Speciation_Pka, self).clean()
		# phLo = float(cleanedData.get('pKa_pH_lower'))
		# phHi = float(cleanedData.get('pKa_pH_upper'))
		# if phLo >= phHi:
		# 	self.add_error('pKa_pH_lower', "pH lower must be < pH upper")
		# 	self.add_error('pKa_pH_upper', "pH upper must be > pH lower")

		# +++ Django 1.6 Way +++
		cleanedData = super(CTS_Speciation_Pka, self).clean()
		pkaChkbox = cleanedData.get('')
		phLo = cleanedData.get('pKa_pH_lower')
		phHi = cleanedData.get('pKa_pH_upper')
		if phLo >= phHi:
			self._errors["pKa_pH_lower"] = self.error_class(["pH lower must be < pH upper"])
			self._errors["pKa_pH_upper"] = self.error_class(["pH upper must be < pH lower"])

			# these fields are no longer valid. remove them from the cleaned data:
			del cleanedData["pKa_pH_lower"]
			del cleanedData["pKa_pH_upper"]

		return cleanedData



# tautomerization table
@parsleyfy
class CTS_Speciation_Tautomer(forms.Form):

	tautomer_maxNoOfStructures = forms.FloatField (
						label='Maximum Number of Structures', 
						initial=100,
						min_value=1,
						max_value=100,
					)

	tautomer_pH = forms.FloatField (
						label='at pH',
						initial=7.0,
						min_value=0,
						max_value=14,
					)

	tautomer_chkbox = forms.BooleanField (
						label='', 
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False,
					)


# stereoisomer table
@parsleyfy
class CTS_Speciation_Stereoisomers(forms.Form):

	stereoisomers_maxNoOfStructures = forms.FloatField (
						label='Maximum Number of Structures',
						initial=100,
						min_value=1,
						max_value=100,
					)

	stereoisomer_chkbox = forms.BooleanField (
						label='', 
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False,
					)

class ChemspecInp(CTS_Chemical_Structure, CTS_Speciation_Pka, CTS_Speciation_Tautomer, CTS_Speciation_Stereoisomers):
	pass