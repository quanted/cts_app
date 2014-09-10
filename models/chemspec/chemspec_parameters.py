# -*- coding: utf-8 -*-
"""
@author: J.Flaishans
"""
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe
import logging


def tmpl_chemstructCTS():
	tmpl_chemstructCTS = """
		<div id="chemEditLookup">
		<table class="input_table tab tab_Chemical">
			<tr>
				<td colspan="2"><span>{{ header }}</span>
				<input id="setSmilesButton" class="tab_chemicalButtons" type="button" value="Enter a SMILES, IUPAC or CAS# and click here" onClick="importMol()"></td>
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
	<table class="input_table tab tab_Speciation" style="display:none">
		<tr><th colspan="2" class="ctsInputHeader">{{ header }}</th></tr>
	{% for field in form %}
		<tr><th>{{ field.label_tag }}</th><td>{{ field }}</td></tr>
	{% endfor %}
	</table>
	"""
	return tmpl_speciationCTS

tmpl_speciationCTS = Template(tmpl_speciationCTS())
tmpl_chemstructCTS = Template(tmpl_chemstructCTS())

# Method(s) called from *_inputs.py
def form():
	form_cts_chemical_structure = cts_chemical_structure()
	html = tmpl_chemstructCTS.render(Context(dict(form=form_cts_chemical_structure, header=mark_safe("Lookup Chemical")))) 
	form_cts_speciation_pKa = cts_speciation_pKa()
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_pKa, header=mark_safe("Ionization Constants (p<i>K</i>a) Parameters"))))
	form_cts_speciation_tautomer = cts_speciation_tautomer()
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_tautomer, header="Dominate Tautomer Distribution")))
	form_cts_speciation_stereoisomers = cts_speciation_stereoisomers()
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_stereoisomers, header="Stereoisomers")))
	return html


# Chemical Editor
class cts_chemical_structure(forms.Form):
	chem_struct = forms.CharField(widget=forms.Textarea (attrs={'cols':50, 'rows':2}), initial='O=C1NN=C(N1)N(=O)=O', label='Chemical Structure')

# Speciation
class cts_speciation_pKa(forms.Form):
	pKa_decimals = forms.FloatField(label='Number of Decimals', initial='2')
	pKa_pH_lower = forms.FloatField(label='pH Lower Limit', initial='0')
	pKa_pH_upper = forms.FloatField(label='pH Upper Limit', initial='14')
	pKa_pH_increment = forms.FloatField(label='pH Step Size', initial='0.2')

	pH_microspecies = forms.FloatField(label='Generate Major Microspeices at pH', initial='7.0')

	isoelectricPoint_pH_increment = forms.FloatField(label=mark_safe('Isoelectric Point (pl) <br> pH Step Size for Charge Distribution'), initial='0.5')

class cts_speciation_tautomer(forms.Form):
	tautomer_maxNoOfStructures = forms.FloatField(label='Maximum Number of Structures', initial='100')
	tautomer_maxNoOfStructures_pH = forms.FloatField(label='at pH', initial='7.0')

class cts_speciation_stereoisomers(forms.Form):
	stereoisomers_maxNoOfStructures = forms.FloatField(label='Maximum Number of Structures', initial='100')