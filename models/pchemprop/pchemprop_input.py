"""
doc stuff for pchemprop_input.py
"""
import django
from django import forms
from django.template.loader import render_to_string
import logging


def pchempropInputPage(request, model='', header='Structural chemspec', formData=None):
    import pchemprop_parameters
    from models.chemspec import chemspec_parameters


    html = render_to_string('04uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js

    html = html + render_to_string('cts-jquery.html', {}) 

    html = html + render_to_string('04uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header+' Inputs'
    })

    html = html + render_to_string('04uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'ChemCalcs'],
                'tab_label': ['Chemical Editor', 'p-Chem Calculator']
                }
            })

    # chemspec inputs
    html = html + str(chemspec_parameters.form()) # Loads the Chemical Speciation tables to the page
    html = html + render_to_string('cts.html', {})

    # pchemprop inputs
    html = html + render_to_string('cts_pchem.html', {})
    html = html + str(pchemprop_parameters.form()) # str(pchemprop_properties.form()) returns html table with ids

    html = html + render_to_string('04ubercts_end.html', {'sub_title': 'Submit'})
    
    # Check if tooltips dictionary exists
    # try:
    #     import pchemprop_tooltips
    #     hasattr(pchemprop_tooltips, 'tooltips')
    #     tooltips = pchemprop_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html
