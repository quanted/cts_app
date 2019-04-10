import os
from django import forms
from django.template.loader import render_to_string
from . import gentrans_parameters
from ..chemspec import chemspec_parameters
from ...cts_calcs.chemical_information import ChemInfo

# Instantiates ChemInfo class for building cheminfo results table:
chem_info = ChemInfo()

jchem_server = os.environ.get('CTS_JCHEM_SERVER')


def gentransInputPage(request, model='', header='Generate Transformation Pathways', formData=None):

    html = render_to_string('04cts_uberinput_jquery.html', { 'model': model }) # loads scripts_gentrans.js
    html = html + render_to_string('04cts_uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header
    }, request=request)

    html = html + render_to_string('04cts_uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ["Chemical", "ReactionPathSim"],
                'tab_label': ['Chemical Editor', 'Reaction Pathway Simulator'],
                },
            'nextTabName': 'Reaction Pathway Simulator'
            })

    html = html + str(chemspec_parameters.form(formData)) # Loads the Chemical Speciation tables to the page
    html = html + render_to_string('cts_cheminfo.html',
        {
            'chem_objects': chem_info.chem_obj,
            'jchem_server': jchem_server
        })
    html = html + str(gentrans_parameters.form(formData))
    html = html + render_to_string('04cts_uberinput_tabbed_end.html', {'sub_title': 'Submit'})

    return html