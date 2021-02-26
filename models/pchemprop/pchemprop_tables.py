import datetime
import json
import os
import logging

from django.template import Context, Template, engines
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from . import pchemprop_parameters
from ...cts_calcs.chemical_information import ChemInfo
from ..cts_pchem_definitions import pchem_defs
from django.conf import settings



# cheminfo instance for building user-inputs table:
chem_info = ChemInfo()



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


# structTmpl = Template(getStructInfoTemplate())
structTmpl = engines['django'].from_string(getStructInfoTemplate())
inTmpl = Template(getInputTemplate())


def table_all(pchemprop_obj):
    html_all = '<br>'
    html_all += '<script src="/static_qed/cts/js/scripts_pchemprop.js" type="text/javascript"></script>'
    html_all += render_to_string('cts_downloads.html', {'run_data': mark_safe(json.dumps(pchemprop_obj.run_data))})
    html_all += input_struct_table(pchemprop_obj)
    html_all += output_pchem_table(pchemprop_obj)

    # Creates popup divs for p-chem table using qtip2 JS library:
    html_all += render_to_string('cts_pchem_definitions_popups.html', {'pchem_defs': pchem_defs})

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

    html += inTmpl.render(Context(dict(data=chem_info.create_cheminfo_table(pchemprop_obj), heading="Molecular Information")))
    # html += inTmpl.render(Context({'data': getInputData(pchemprop_obj), heading="Molecular Information"}))

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
    <H3 class="out_1 collapsible" id="section1"><span></span>Physicochemical Properties Results</H3>
    <div class="out_">
    <script>
    $(document).ready(function() {
        $("#pchemprop_table").css('display', 'table');
    });
    </script>
    """

    kow_ph = 7.4
    if pchemprop_obj.kow_ph:
        kow_ph = round(float(pchemprop_obj.kow_ph), 1)

    pchemHTML = render_to_string('cts_pchem.html', {})
    pchemHTML += str(pchemprop_parameters.form(None))
    pchemHTML = pchemHtmlTemplate().render(Context(dict(pchemHtml=pchemHTML)))

    html += pchemHTML

    html += render_to_string('cts_pchemprop_requests.html', {
                                    "time": pchemprop_obj.jid,
                                    "kow_ph": kow_ph,
                                    "structure": pchemprop_obj.smiles,
                                    "name": pchemprop_obj.name,
                                    "mass": pchemprop_obj.mass,
                                    "formula": pchemprop_obj.formula,
                                    "checkedCalcsAndProps": pchemprop_obj.checkedCalcsAndPropsDict,
                                    'nodes': None,
                                    'speciation_inputs': None,
                                    'workflow': 'pchemprop',
                                    'run_type': 'single',
                                    'nodejs_host': settings.NODEJS_HOST,
                                    'nodejs_port': settings.NODEJS_PORT
                                }
                            )

    html += """
        <br>
        <input type="button" value="Calculate data" class="submit input_button btn-pchem" id="btn-pchem-data">
        <input type="button" value="Clear data" class="input_button btn-pchem" id="btn-pchem-cleardata">
        <input type="button" value="Cancel" class="input_button btn-pchem" id="btn-pchem-cancel">
    </div>
    """
    return html


def pchemHtmlTemplate():
    # do this when inserting it into html (see metaboliteInfoTmpl):
    pchem_html = """
    {% autoescape off %}{{pchemHtml}}{% endautoescape %}
    """
    return Template(pchem_html)