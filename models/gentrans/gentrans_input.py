import os
from django import forms
from django.template.loader import render_to_string
from . import gentrans_parameters
from ..chemspec import chemspec_parameters
from ...cts_calcs.chemical_information import ChemInfo

# Instantiates ChemInfo class for building cheminfo results table:
chem_info = ChemInfo()

jchem_server = os.environ.get('MARVIN_PROXY')  # url for marvinsketchjs operations


def gentransInputPage(request, model='gentrans', header='Generate Transformation Pathways', formData=None):
    orig_model = model
    if model == 'biotrans':
        model = 'gentrans'

    html = render_to_string('04cts_uberinput_jquery.html',
        { 
            'model': model,
            'ENV_NAME': os.environ.get('ENV_NAME')
        }
    ) # loads scripts_gentrans.js
    html = html + render_to_string('04cts_uberinput_start_tabbed.html', {
            # 'model': model,
            'model': orig_model,
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
    html = html + str(gentrans_parameters.form(formData, orig_model))
    html = html + render_to_string('04cts_uberinput_tabbed_end.html', {'sub_title': 'Submit'})

    return html