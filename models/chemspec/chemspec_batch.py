import json
import os
import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ..chemspec import chemspec_output
from ..chemspec import chemspec_parameters
from ..pchemprop import pchemprop_parameters


def chemspecBatchInputPage(request, model='', header='Chemical Speciation Properties', formData=None):
    """
    Currently, I'm using these model specific batch input page functions
    for drawing the models' unique input selection. For chemspec, the p-chem
    appears after the user has uploaded a chemical file for batch
    """
    # for chemspec batch, use p-chem for selecting inputs for batch data:
    html = """
    <div id="pchem_batch_wrap" hidden>
        <h3>Edit speciation parameters for batch chemicals</h3>
    """
 
    html += str(chemspec_parameters.form(None))

    html += """
        <div class="input_nav">
            <div class="input_right">
                <input type="button" value="Clear" id="clearbutton" class="input_button">
                <input class="submit input_button" type="submit" value="Submit">
            </div>
        </div>
    </div>
    """

    return html


def chemspecBatchOutputPage(request, model='', header='Chemical Speciation Properties', formData=None):

    chemspec_obj = chemspec_output.chemspecOutputPage(request)
    batch_chemicals = request.POST.get('nodes')  # expecting list of nodes (change name??)

    if not batch_chemicals:
        batch_chemicals = []
    if isinstance(batch_chemicals, str):
        batch_chemicals = json.loads(batch_chemicals)

    html = render_to_string('cts_app/cts_downloads.html', 
        {'run_data': chemspec_obj.run_data}, request=request)

    html += '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'

    html +=  render_to_string('cts_app/cts_pchemprop_requests.html', 
        {
            'checkedCalcsAndProps': {},
            'speciation_inputs': chemspec_obj.speciation_inputs,
            'nodes': batch_chemicals,
            'workflow': "chemspec",
            'run_type': "batch",
            'run_data': chemspec_obj.run_data,
            'nodejs_host': os.getenv("NODEJS_HOST"),
            'nodejs_port': os.getenv("NODEJS_PORT")
        }
    )

    html += render_to_string('cts_app/cts_gentrans_tree.html', {'gen_max': 0})


    return html