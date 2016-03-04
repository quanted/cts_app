"""
yeah (np)
"""
import django
from django import forms
from django.template.loader import render_to_string
import logging    

    
def chemspecInputPage(request, model='', header='Chemical Speciation', formData=None):
    import chemspec_parameters

    html = render_to_string('04uberinput_jquery.html', { 'model': model }) # Loads scripts_chemspec.js
    html = html + render_to_string('cts-jquery.html', {}) # js for cts (across workflows)
    html = html + render_to_string('04uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header
    })

    html = html + render_to_string('04uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'Speciation'],
                'tab_label': ['Chemical Editor', 'Chemical Speciation']
                },
            'nextTabName': 'Chemical Speciation'
            })
    
    # html = html + str(chemspec_parameters.ChemspecInp(formData))

    html = html + str(chemspec_parameters.form(formData)) # Loads the Chemical Speciation tables to the page

    # html = html + render_to_string('cts_inputs_validation.html', {})

    html = html + render_to_string('cts.html', {}) # Builds marvin js and results table 

    html = html + render_to_string('04uberinput_tabbed_end.html', {'sub_title': 'Submit'})
    

    # Check if tooltips dictionary exists
    # try:
    #     import chemspec_tooltips
    #     hasattr(chemspec_tooltips, 'tooltips')
    #     tooltips = chemspec_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html