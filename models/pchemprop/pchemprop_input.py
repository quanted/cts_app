"""
doc stuff
"""
import django
from django import forms
from django.template.loader import render_to_string


def pchempropInputPage(request, model='', header='Structural Analysis', formData=None):
    import pchemprop_parameters
    from models.analysis import analysis_parameters


    html = render_to_string('04uberinput_jquery.html', { 'model': model})

    html = render_to_string('04uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header+' Inputs'
    })

    html = html + render_to_string('04uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'Speciation', 'ChemCalcs', 'Transform'],
                'tab_label': ['Chemical Editor', 'Chemical Speciation', 'Chemical Calculators', 'Transformation Pathways']
                }
            })

    html = html + render_to_string('cts.html', {})

    html = html + str(analysis_parameters.form())
    html = html + render_to_string('cts_pchem.html', {})
    html = html + str(pchemprop_parameters.form())

    html = html + render_to_string('04ubercts_end.html', {'sub_title': 'Submit'})
    
    # Check if tooltips dictionary exists
    try:
        import pchemprop_tooltips
        hasattr(pchemprop_tooltips, 'tooltips')
        tooltips = pchemprop_tooltips.tooltips
    except:
        tooltips = {}
    html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html
