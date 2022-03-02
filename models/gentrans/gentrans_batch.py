import json
import logging
import os

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from . import gentrans_parameters
from . import gentrans_output
from ..pchemprop import pchemprop_output


def gentransBatchInputPage(request, model='', header='Transformation Products', formData=None):
    """
    Currently, I'm using these model specific batch input page functions
    for drawing the models' unique input selection. For pchemprop, the p-chem
    appears after the user has uploaded a chemical file for batch
    """

    html = """
    <script src="/static_qed/cts_app/js/scripts_pchemprop.js"></script>
    <div id="pchem_batch_wrap" hidden>
        <h3>1. Select transformation pathways for batch chemicals</h3>
    """

    html += str(gentrans_parameters.form(formData))

    html += """
        <br>
        <h3>2. Select physicochemical properties for transformation products</h3>
    """
    html += render_to_string('cts_app/cts_pchem.html', {})

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


def gentransBatchOutputPage(request, model='', header='Transformation Products', formData=None):

    # get all the fields from the form in the request, then
    # instantiate model object to get checkedCalcsAndProps dict.
    # render said dict into cts_pchemprop_ajax_calls template

    # get transformation products through gentrans_model,
    # then use cts_gentrans_tree and cts_pchemprop_ajax_calls to
    # get pchem data for batch mode csv output

    batch_chemicals = request.POST.get('nodes')  # expecting list of nodes (change name??)

    if not batch_chemicals:
        batch_chemicals = []
    if isinstance(batch_chemicals, str):
        batch_chemicals = json.loads(batch_chemicals)

    gentrans_obj = gentrans_output.gentransOutputPage(request)

    metabolizer_post = gentrans_obj.metabolizer_request_post
    metabolizer_post['structure'] = gentrans_obj.smiles

    # get pchemprop model for cts_gentrans_tree/cts_pchemprop_ajax_calls on output page..
    pchemprop_obj = pchemprop_output.pchempropOutputPage(request)  # backend calc/prop dict generation

    # html = render_to_string('cts_app/cts_downloads.html', 
    #     {'run_data': mark_safe(json.dumps(gentrans_obj.run_data))})

    html = render_to_string('cts_app/cts_downloads.html', {'run_data': pchemprop_obj.run_data})

    html += '<script src="/static_qed/cts_app/js/scripts_pchemprop.js" type="text/javascript" ></script>'
    html += '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'

    html += render_to_string('cts_app/cts_gentrans_tree.html', {'gen_max': gentrans_obj.gen_limit})

    # for pchemprop batch, use p-chem for selecting inputs for batch data:
    html +=  render_to_string('cts_app/cts_pchemprop_requests.html', 
        {
            'structure': mark_safe(gentrans_obj.smiles),
            'calc': gentrans_obj.calc,
            'checkedCalcsAndProps': pchemprop_obj.checkedCalcsAndPropsDict,
            'kow_ph': pchemprop_obj.kow_ph,
            'nodes': batch_chemicals,
            'workflow': "gentrans",
            'run_type': "batch",
            'run_data': pchemprop_obj.run_data,
            'speciation_inputs': 'null',
            'nodejs_host': os.getenv("NODEJS_HOST"),
            'nodejs_port': os.getenv("NODEJS_PORT"),
            'service': "getTransProducts",
            'metabolizer_post': metabolizer_post
        }
    )

    html += """
    <div id="cont" hidden>
        <div id="center-cont">
            <!-- the canvas container -->
            <div id="infovis"></div>
        </div>
        <div id="log"></div>
    </div>
    """

    return html