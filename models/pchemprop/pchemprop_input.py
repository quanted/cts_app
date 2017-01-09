"""
doc stuff for pchemprop_input.py
"""
import django
from django import forms
from django.template.loader import render_to_string
import logging


def pchempropInputPage(request, model='', header='P-Chem Properties', formData=None):
    import pchemprop_parameters
    from cts_app.models.chemspec import chemspec_parameters


    html = render_to_string('04cts_uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js

    html = html + render_to_string('04cts_uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header
    })

    html = html + render_to_string('04cts_uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'ChemCalcs'],
                'tab_label': ['Chemical Editor', 'P-Chem Calculators']
                },
            'nextTabName': 'P-Chem Calculators'
            })

    # chemspec inputs
    html = html + str(chemspec_parameters.form(formData)) # Loads the Chemical Speciation tables to the page
    html = html + render_to_string('cts.html', {})

    # pchemprop inputs
    html = html + render_to_string('cts_pchem.html', {})
    # html = html + str(pchemprop_parameters.form(formData)) # str(pchemprop_properties.form()) returns html table with ids

    html = html + render_to_string('04cts_ubercts_end.html', {'sub_title': 'Submit'})
    
    # Check if tooltips dictionary exists
    # try:
    #     import pchemprop_tooltips
    #     hasattr(pchemprop_tooltips, 'tooltips')
    #     tooltips = pchemprop_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html = html + render_to_string('05cts_ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html
