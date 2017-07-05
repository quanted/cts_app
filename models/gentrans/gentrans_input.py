"""
yeah (np)
"""
import django
from django import forms
from django.template.loader import render_to_string
from . import gentrans_parameters
from ..chemspec import chemspec_parameters


def gentransInputPage(request, model='', header='Generate Transformation Pathways', formData=None):

    html = render_to_string('04cts_uberinput_jquery.html', { 'model': model }) # loads scripts_gentrans.js
    html = html + render_to_string('04cts_uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header
    })

    html = html + render_to_string('04cts_uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ["Chemical", "ReactionPathSim"],
                'tab_label': ['Chemical Editor', 'Reaction Pathway Simulator'],
                },
            'nextTabName': 'Reaction Pathway Simulator'
            })

    html = html + str(chemspec_parameters.form(formData)) # Loads the Chemical Speciation tables to the page
    html = html + render_to_string('cts.html', {}) # Builds Marvin JS, lookup table, and results table
    html = html + str(gentrans_parameters.form(formData))
    html = html + render_to_string('04cts_uberinput_tabbed_end.html', {'sub_title': 'Submit'})

    # Check if tooltips dictionary exists
    # try:
    #     import gentrans_tooltips
    #     hasattr(gentrans_tooltips, 'tooltips')
    #     tooltips = gentrans_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html = html + render_to_string('05cts_ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html