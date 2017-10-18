"""
doc stuff for pchemprop_input.py
"""

from django.template.loader import render_to_string
from ..chemspec import chemspec_parameters

def pchempropInputPage(request, model='', header='Physical-Chemical Properties', formData=None):

    html = render_to_string('04cts_uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js

    html = html + render_to_string('04cts_uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header
    }, request=request)

    html = html + render_to_string('04cts_uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'ChemCalcs'],
                'tab_label': ['Chemical Editor', 'Physical-Chemical Calculators']
                },
            'nextTabName': 'Physical-Chemical Calculators'
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
