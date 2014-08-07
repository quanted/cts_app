"""
Djangofied on 30 July 2014 

@author: np
"""

from django.template.loader import render_to_string


def efsInputPage(request, model='', header=''):
    import efs_parameters, efs_tooltips

    html = render_to_string('04uberinput_jquery.html', { 'model': model })
    html = html + render_to_string('04uberinput_start.html', {
            'model':model, 
            'model_attributes': header+' Inputs'})
    html = html + render_to_string('efs_ubertool_config_input.html', {})
    html = html + str(efs_parameters.EFSInp())
    html = html + render_to_string('04uberinput_end.html', {'sub_title': 'Submit'})
    html = html + render_to_string('efs_ubertool_config.html', {})
    # Check if tooltips dictionary exists
    if hasattr(efs_tooltips, 'tooltips'):
        tooltips = efs_tooltips.tooltips
    else:
        tooltips = {}
    html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})    

    return html