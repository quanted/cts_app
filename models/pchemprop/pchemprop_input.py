"""
doc stuff for pchemprop_input.py
"""

from django.template.loader import render_to_string
from ..chemspec import chemspec_parameters
from ..cts_pchem_definitions import pchem_defs

def pchempropInputPage(request, model='', header='Physicochemical Properties', formData=None):

    html = render_to_string('04cts_uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js

    html = html + render_to_string('04cts_uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header
    }, request=request)

    html = html + render_to_string('04cts_uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'ChemCalcs'],
                'tab_label': ['Chemical Editor', 'Physicochemical Calculators']
                },
            'nextTabName': 'Physicochemical Calculators'
            })

    # chemspec inputs
    html = html + str(chemspec_parameters.form(formData))
    html = html + render_to_string('cts_cheminfo.html', {})

    # pchemprop inputs
    html = html + render_to_string('cts_pchem.html', {})
    
    # Creates popup divs for p-chem table using qtip2 JS library:
    html += render_to_string('cts_pchem_definitions_popups.html', 
        {'pchem_defs' :pchem_defs})

    html = html + render_to_string('04cts_ubercts_end.html', {'sub_title': 'Submit'})
    
    return html
