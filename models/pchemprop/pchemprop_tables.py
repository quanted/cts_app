from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import pchemprop_parameters
import json
import os



def getInputData(pchemprop_obj):
    data = [
        {'Entered chemical': pchemprop_obj.chem_struct},
        {'SMILES': pchemprop_obj.smiles},
        {'Initial SMILES': pchemprop_obj.orig_smiles},
        {'IUPAC': pchemprop_obj.name}, 
        {'Formula': pchemprop_obj.formula}, 
        {'Mass': pchemprop_obj.mass},
        {'Exact Mass': pchemprop_obj.exact_mass}
    ]
    return data


def getStructInfoTemplate():
    structInfoTemplate ="""
        <dl class="shiftRight">
        {% for label, value in data %}
            <dd>
            <b>{{label}}</b> {{value|default:"none"}}
            </dd>
        {% endfor %}
        </dl>
        """
    return structInfoTemplate


def getInputTemplate():
    input_template = """
    <table class="ctsTableStylin" style="display:inline-block;">
    <th colspan="2" class="alignLeft">{{heading}}</th>
    {% for keyval in data %}
        {% for label, value in keyval.items %}
            <tr>
            <td>{{label}}</td> <td>{{value|default:"none"}}</td>
            </tr>
        {% endfor %}
    {% endfor %}
    </table>
    """
    return input_template


structTmpl = Template(getStructInfoTemplate())
inTmpl = Template(getInputTemplate())


def table_all(pchemprop_obj):
    html_all = '<br>'
    html_all += '<script src="/static/stylesheets/scripts_pchemprop.js" type="text/javascript"></script>'
    html_all += render_to_string('cts_downloads.html', {'run_data': mark_safe(json.dumps(pchemprop_obj.run_data))})
    html_all += input_struct_table(pchemprop_obj)
    html_all += output_pchem_table(pchemprop_obj)
    return html_all


def input_struct_table(pchemprop_obj):
    """
    structure information table (smiles, iupac, etc.)
    """

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
    <div class="info_image_wrap">
    """

    # attempting to add image to right of user inputs table:
    html += pchemprop_obj.parent_image

    html += inTmpl.render(Context(dict(data=getInputData(pchemprop_obj), heading="Molecular Information")))

    html += """
    </div>
    </div>
    """
    return html


def output_pchem_table(pchemprop_obj):
    """
    results of chemaxon properties 
    """
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section1"><span></span>P-Chem Properties Results</H3>
    <div class="out_">
    <script>
    $(document).ready(function() {
        $("#pchemprop_table").css('display', 'table');
    });
    </script>
    """

    kow_ph = 0.0
    if pchemprop_obj.kow_ph:
        kow_ph = round(float(pchemprop_obj.kow_ph), 1)

    pchemHTML = render_to_string('cts_pchem.html', {})
    pchemHTML += str(pchemprop_parameters.form(None))
    pchemHTML = pchemHtmlTemplate().render(Context(dict(pchemHtml=pchemHTML)))

    html += pchemHTML

    html += render_to_string('cts_pchemprop_ajax_calls.html', {
                                    "time": pchemprop_obj.jid,
                                    "kow_ph": kow_ph,
                                    "structure": mark_safe(pchemprop_obj.smiles),
                                    "name": mark_safe(pchemprop_obj.name),
                                    "mass": pchemprop_obj.mass,
                                    "formula": pchemprop_obj.formula,
                                    "checkedCalcsAndProps": mark_safe(pchemprop_obj.checkedCalcsAndPropsDict),
                                    'nodes': 'null',
                                    'speciation_inputs': 'null'
                                    # "test_results": mark_safe(json.dumps(pchemprop_obj.test_results))
                            })
    html += """
        <br>
        <input type="button" value="Get data" class="submit input_button btn-pchem" id="btn-pchem-data">
        <input type="button" value="Clear data" class="input_button btn-pchem" id="btn-pchem-cleardata">
        <input type="button" value="Cancel" class="input_button btn-pchem" id="btn-pchem-cancel">
        <br>
        <p class="gentransError">Must right-click a metabolite first</p>
        <p class="selectNodeForData">Select (right-click) a node to view p-chem data</p>
    </div>
    """
    return html


def pchemHtmlTemplate():
    # do this when inserting it into html (see metaboliteInfoTmpl):
    pchem_html = """
    {% autoescape off %}{{pchemHtml}}{% endautoescape %}
    """
    return Template(pchem_html)


def timestamp(pchemprop_obj="", batch_jid=""):
    if pchemprop_obj:
        st = datetime.datetime.strptime(pchemprop_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Calculate P-Chem Properties Version {}</a> (Beta)<br>
    """.format(os.environ['CTS_VERSION'])
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html