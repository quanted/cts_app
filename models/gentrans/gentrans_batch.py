from django.conf import settings
from django.template.loader import render_to_string
from models.gentrans import gentrans_parameters
import json


def gentransBatchInputPage(request, model='', header='Transformation Products', formData=None):
    """
    Currently, I'm using these model specific batch input page functions
    for drawing the models' unique input selection. For pchemprop, the p-chem
    appears after the user has uploaded a chemical file for batch
    """

    html = """
    <script src="/static/stylesheets/scripts_pchemprop.js"></script>
    <div id="pchem_batch_wrap" hidden>
        <h3>1. Select transformation pathways for batch chemicals</h3>
    """

    html += str(gentrans_parameters.form(formData))

    # html += """
    #     <br>
    #     <h3>2. Select any p-chem properties for transformation products</h3>
    # """

    html += """
        <br>
        <h3>2. P-Chem properties for transformation products coming soon..</h3>
    """

    # html += render_to_string('cts_pchem.html', {})

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

    from models.gentrans import gentrans_output
    from models.pchemprop import pchemprop_output
    from django.utils.safestring import mark_safe


    # get transformation products through gentrans_model,
    # then use cts_gentrans_tree and cts_pchemprop_ajax_calls to
    # get pchem data for batch mode csv output

    batch_chemicals = request.POST.get('nodes')  # expecting list of nodes (change name??)

    if not batch_chemicals:
        batch_chemicals = []

    # for chemical in batch_chemicals:
    #     # get transformation products (synchronous!):

    # request.POST.update({'run_type': "batch"})
    gentrans_obj = gentrans_output.gentransOutputPage(request)

    # get pchemprop model for cts_gentrans_tree/cts_pchemprop_ajax_calls on output page..
    pchemprop_obj = pchemprop_output.pchempropOutputPage(request)  # backend calc/prop dict generation

    # html = render_to_string('cts_downloads.html', 
    #     {'run_data': mark_safe(json.dumps(gentrans_obj.run_data))})

    html = render_to_string('cts_downloads.html', {'run_data': mark_safe(json.dumps(pchemprop_obj.run_data))})

    html += '<script src="/static/stylesheets/scripts_pchemprop.js" type="text/javascript" ></script>'
    html += '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'

    html += render_to_string('cts_gentrans_tree.html', {'gen_max': gentrans_obj.gen_limit})

    # for pchemprop batch, use p-chem for selecting inputs for batch data:
    html +=  render_to_string('cts_pchemprop_requests.html', 
        {
            'checkedCalcsAndProps': mark_safe(pchemprop_obj.checkedCalcsAndPropsDict),
            'kow_ph': pchemprop_obj.kow_ph,
            'nodes': mark_safe(batch_chemicals),
            'workflow': "gentrans",
            'run_type': "batch",
            'run_data': pchemprop_obj.run_data,
            'speciation_inputs': 'null',
            'nodejs_host': settings.NODEJS_HOST,
            'nodejs_port': settings.NODEJS_PORT
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