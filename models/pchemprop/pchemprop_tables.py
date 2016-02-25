from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import pchemprop_parameters
import json




def getInputData(pchemprop_obj):
    data = {
        'SMILES': pchemprop_obj.smiles,
        'IUPAC': pchemprop_obj.name,
        'Formula': pchemprop_obj.formula,
        'Mass': pchemprop_obj.mass
    }
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
    <table class="ctsTableStylin">
    <th colspan="2" class="alignLeft">{{heading}}</th>
    {% for label, value in data.items %}
        <tr>
        <td>{{label}}</td> <td>{{value|default:"none"}}</td>
        </tr>
    {% endfor %}
    </table>
    """
    return input_template


structTmpl = Template(getStructInfoTemplate())
inTmpl = Template(getInputTemplate())


def table_all(pchemprop_obj):
    html_all = '<br>'
    html_all += '<script src="/static/stylesheets/scripts_pchemprop.js" type="text/javascript"></script>'
    html_all += input_struct_table(pchemprop_obj)
    html_all += output_pchem_table(pchemprop_obj)
    # html_all += render_to_string('cts_display_raw_data.html', {'rawData': pchemprop_obj.rawData}) # temporary
    return html_all


def input_struct_table(pchemprop_obj):
    """
    structure information table (smiles, iupac, etc.)
    """

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
    """
    html += inTmpl.render(Context(dict(data=getInputData(pchemprop_obj), heading="Molecular Information")))
    html += """
    </div>
    """
    return html


def output_pchem_table(pchemprop_obj):
    """
    results of chemaxon properties 
    """
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section1"><span></span>p-Chem Properties Results</H3>
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

    # html += render_to_string('cts_pchemprop_cleanOutputTable.html', {"kow_ph": kow_ph})
    html += render_to_string('cts_pchemprop_ajax_calls.html', {
                                    "time": pchemprop_obj.jid,
                                    "kow_ph": kow_ph,
                                    "structure": mark_safe(pchemprop_obj.chem_struct),
                                    "name": mark_safe(pchemprop_obj.name),
                                    "mass": pchemprop_obj.mass,
                                    "formula": pchemprop_obj.formula,
                                    "checkedCalcsAndProps": mark_safe(pchemprop_obj.checkedCalcsAndPropsDict),
                                    # "test_results": mark_safe(json.dumps(pchemprop_obj.test_results))
                            })
    html += """
        <br>
        <input type="button" value="Get data" class="submit input_button btn-pchem" id="btn-pchem-data">
        <input type="button" value="Clear data" class="input_button btn-pchem" id="btn-pchem-cleardata">
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
        <b>Generate Transformation Pathways Version 1.0</a> (Alpha)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html