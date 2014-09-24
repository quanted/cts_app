"""
yeah (np)
"""
import django
from django import forms
from django.template.loader import render_to_string    


    
def gentransInputPage(request, model='', header='Chemical Speciation', formData=None):
    import gentrans_parameters
    from models.pchemprop import pchemprop_parameters
    from models.chemspec import chemspec_parameters

    html = render_to_string('04uberinput_jquery.html', { 'model': model }) # loads scripts_gentrans.js
    html = html + render_to_string('cts-jquery.html', {})
    html = html + render_to_string('04uberinput_start_tabbed.html', {
            'model': model,
            'model_attributes': header+' Inputs'
    })
    
    html = html + render_to_string('04uberinput_tabbed_nav.html', {
            'nav_dict': {
                'class_name': ["Chemical", "ReactionPathSim", "ChemCalcs", "ReactionRateCalc"],
                'tab_label': ['Chemical Editor', 'Reaction Pathway Simulator', 'p-Chem Calculator', 'Reaction Rate Calculator'],
                }
            })

    html = html + str(chemspec_parameters.form()) # Loads the Chemical Speciation tables to the page

    html = html + render_to_string('cts.html', {}) # Builds Marvin JS, lookup table, and results table
    
    # reaction pathway simulator segment:
    html = html + render_to_string('cts_reaction_path_sim.html', {})
    html = html + str(gentrans_parameters.form())

    # p-chem calculator piece:
    html = html + render_to_string('cts_pchem.html', {})
    html = html + str(pchemprop_parameters.form())

    #html = html + str(gentrans_parameters.form())
#        html = html + render_to_string('jschemeditor.html', {})
    #html = html + render_to_string('04ubercts_end.html', {'sub_title': 'Submit'})
    html = html + render_to_string('04uberinput_tabbed_end.html', {'sub_title': 'Submit'})

    # Check if tooltips dictionary exists
    # try:
    #     import gentrans_tooltips
    #     hasattr(gentrans_tooltips, 'tooltips')
    #     tooltips = gentrans_tooltips.tooltips
    # except:
    #     tooltips = {}
    # html = html + render_to_string('05ubertext_tooltips_right.html', {'tooltips':tooltips})

    return html