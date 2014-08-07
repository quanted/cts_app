"""

"""
import django
from django import forms
from django.template.loader import render_to_string    


    
def analysisInputPage(request, model='', header='Structural Analysis', formData=None):
    import analysis_parameters

    # html = render_to_string('04uberinput_jquery.html', { 'model': model })
    html = render_to_string('04uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header+' Inputs'
    })
    
    html = html + render_to_string('04uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ['Chemical', 'Speciation'],
                'tab_label': ['Chemical Editor', 'Chemical Speciation']
                }
            })

    html = html + render_to_string('cts.html', {})
    html = html + str(analysis_parameters.form())
#        html = html + render_to_string('jschemeditor.html', {})
    html = html + render_to_string('04ubercts_end.html', {'sub_title': 'Submit'})
    # Check if tooltips dictionary exists
    try:
        import analysis_tooltips
        hasattr(analysis_tooltips, 'tooltips')
        tooltips = analysis_tooltips.tooltips
    except:
        tooltips = {}
    html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html