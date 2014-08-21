# -*- coding: utf-8 -*-
"""
@author: J.Flaishans
"""
import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from django import forms
from django.template import Context, Template
from django.utils.safestring import mark_safe


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

# Method(s) called from *_inputs.py
# def form():
class chemspecInp(forms.Form):
	form_cts_speciation_pKa = cts_speciation_pKa()
	html = tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_pKa, header=mark_safe("Ionization Constants (p<i>K</i>a) Parameters"))))
	form_cts_speciation_tautomer = cts_speciation_tautomer()
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_tautomer, header="Dominate Tautomer Distribution")))
	form_cts_speciation_stereoisomers = cts_speciation_stereoisomers()
	html = html + tmpl_speciationCTS.render(Context(dict(form=form_cts_speciation_stereoisomers, header="Stereoisomers")))
	#return html

# Begin parameters declaration
# Temporary/generic
# class chemspecInp(forms.Form):
	
#     chemical_name = forms.CharField(widget=forms.Textarea (attrs={'cols': 20, 'rows': 2}))
#     body_weight_of_bird = forms.FloatField(required=True,label='NEED TO GET INPUTS.')

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