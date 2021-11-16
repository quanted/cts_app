"""
Input page view for chemical speciation workflow.
"""

import logging
import os
from django import forms
from django.template.loader import render_to_string
from . import chemspec_parameters
from ...cts_calcs.chemical_information import ChemInfo

# Instantiates ChemInfo class for building cheminfo results table:
chem_info = ChemInfo()

jchem_server = os.environ.get('MARVIN_PROXY')  # url for marvinsketchjs operations

    

def chemspecInputPage(request, model='', header='Chemical Speciation', formData=None):

    html = render_to_string('cts_app/04cts_uberinput_jquery.html', { 'model': model }) # Loads scripts_chemspec.js

    html = html + render_to_string('cts_app/04cts_uberinput_start_tabbed.html',
        {'model': model, 'model_attributes': header},
        request=request
    )

    html = html + render_to_string('cts_app/04cts_uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'Speciation'],
                'tab_label': ['Chemical Editor', 'Chemical Speciation']
                },
            'nextTabName': 'Chemical Speciation'
            })

    html = html + str(chemspec_parameters.form(formData)) # Loads the Chemical Speciation tables to the page

    html = html + render_to_string('cts_app/cts_cheminfo.html',
        {
            'chem_objects': chem_info.chem_obj,
            'jchem_server': jchem_server
        })

    html = html + render_to_string('cts_app/04cts_uberinput_tabbed_end.html', {'sub_title': 'Submit'})
    
    return html