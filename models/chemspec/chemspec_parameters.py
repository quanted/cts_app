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
				<input id="setSmilesButton" class="tab_chemicalButtons" type="button" value="Enter a SMILES, IUPAC or CAS# and click here"></td>
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

	<table class="input_table tab tab_Speciation" style="display:none">

	{% if name == "cts_speciation_pKa" %}
		<tr><th colspan="2" class="ctsInputHeader">{{ form.pka_chkbox }} {{ header }}</th></tr>
	{% elif name == "cts_speciation_tautomer" %}
		<tr><th colspan="2" class="ctsInputHeader">{{ form.tautomer_chkbox }} {{ header }}</th></tr>
	{% elif name == "cts_speciation_stereoisomers" %}
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
	form_cts_chemical_structure = cts_chemical_structure(formData)
	html = tmpl_chemstructCTS.render(Context(dict(form=form_cts_chemical_structure, header=mark_safe("Lookup Chemical")))) 
	form_cts_speciation_pKa = cts_speciation_pKa(formData)
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_pKa, header=mark_safe("Ionization Constants (p<i>K</i>a) Parameters"))))
	form_cts_speciation_tautomer = cts_speciation_tautomer(formData)
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_tautomer, header="Dominate Tautomer Distribution")))
	form_cts_speciation_stereoisomers = cts_speciation_stereoisomers(formData)
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_stereoisomers, header="Stereoisomers")))
	return html


"""Chemical Editor"""
class cts_chemical_structure(forms.Form):

	chem_struct = forms.CharField (
					widget=forms.Textarea(attrs={'cols':50, 'rows':2}),
					initial='',
					label='Chemical Structure',
					required=True,
					# validators=[]
				)


"""Chemical Speciation"""

# pka table
class cts_speciation_pKa(forms.Form):


	pKa_decimals = forms.FloatField (
						label='Number of Decimals', 
						initial='2', 
						validators=[validation.validate_greaterthan0]
					)

	pKa_pH_lower = forms.FloatField (
						label='pH Lower Limit',
						initial='0'
					)

	pKa_pH_upper = forms.FloatField (
						label='pH Upper Limit',
						initial='14'
					)

	pKa_pH_increment = forms.FloatField (
						label='pH Step Size',
						initial='0.2',
						validators=[validation.validate_greaterthan0]
					)

	pH_microspecies = forms.FloatField (
						label='Generate Major Microspeices at pH',
						initial='7.0'
					)

	isoelectricPoint_pH_increment = forms.FloatField (
						label=mark_safe('Isoelectric Point (pl) <br> pH Step Size for Charge Distribution'),
						initial='0.5'
					)

	# Check box for selecting table
	pka_chkbox = forms.BooleanField (
						label='',
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False
					)

	# custom validation for the whole Form (not just pka table)
	# def clean(self):
		
	# 	cleaned_data = super(cts_speciation_pKa, self).clean()

	# 	pka_chkbox = cleaned_data.get("pka_chkbox")
	# 	tautomer_chkbox = cleaned_data.get("tautomer_chkbox")
	# 	stereoisomer_chkbox = cleaned_data.get("stereoisomer_chkbox")

	# 	logging.warning("FORM " + str(cleaned_data))

	# 	if (pka_chkbox or tautomer_chkbox or stereoisomer_chkbox) == False:
	# 		logging.warning("no checkboxes selected...")
	# 		raise forms.ValidationError("You must select at least one table")

		# if pka_chkbox:
		# 	for field in cleaned_data:
		# 		logging.warning(str(field) + ", " + str(cleaned_data.get(field)))


		# cleaned_data = super(ContactForm, self).clean()
  #       cc_myself = cleaned_data.get("cc_myself")
  #       subject = cleaned_data.get("subject")

  #       if cc_myself and subject:
  #           # Only do something if both fields are valid so far.
  #           if "help" not in subject:
  #               raise forms.ValidationError("Did not send for 'help' in "
  #                       "the subject despite CC'ing yourself.")


# tautomerization table
class cts_speciation_tautomer(forms.Form):

	tautomer_maxNoOfStructures = forms.FloatField (
						label='Maximum Number of Structures', 
						initial='100'
					)

	tautomer_pH = forms.FloatField (
						label='at pH',
						initial='7.0'
					)

	tautomer_chkbox = forms.BooleanField (
						label='', 
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False
					)


# stereoisomer table
class cts_speciation_stereoisomers(forms.Form):

	stereoisomers_maxNoOfStructures = forms.FloatField (
						label='Maximum Number of Structures',
						initial='100'
					)

	stereoisomer_chkbox = forms.BooleanField (
						label='', 
						widget=forms.CheckboxInput(attrs={'class':'alignChkbox'}),
						required=False
					)

class ChemspecInp(cts_chemical_structure, cts_speciation_pKa, cts_speciation_tautomer, cts_speciation_stereoisomers):
	pass