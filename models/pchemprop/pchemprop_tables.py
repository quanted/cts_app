
from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json
import pchemprop_parameters


def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpchem():
    headings = ["props", "klop", "phys", "vg", "weighted"]
    return headings


def gethtmlrowsfromcols(data, headings):
    columns = [data[heading] for heading in headings]
    # get the length of the longest column
    max_len = len(max(columns, key=len))
    for col in columns:
        # padding the short columns with None
        col += [None,] * (max_len - len(col))
    # Then rotate the structure...
    rows = [[col[i] for col in columns] for i in range(max_len)]
    return rows


def getInputData(pchemprop_obj):
    data = {
        "Parameter": ['SMILES:', 'IUPAC:', 'Formula:', 'Mass:'],
        "Value": [pchemprop_obj.smiles, pchemprop_obj.name, pchemprop_obj.formula, pchemprop_obj.mass],
        # "Image": [pchemprop_obj.parentImage]
    }
    return data


def getdjtemplate():
    dj_template ="""
    <table id="pchemprop_table_out" class="input_table tab tab_ChemCalcs">
    <tr>
        <th></th>
        <th>ChemAxon</th>
        <th>EPI Suite</th>
        <th>TEST</th>
        <th>SPARC</th>
        <th>Measured</th>
    </tr>

    {% load set_var %}
    {% set skip = False %}

    {# loops through pchemprop_parameters fields #}
    {% for field in fields %}
        {# conditionals for appending kow_wph and kow_ph fields #}
        {% if field.html_name == "kow_wph" %}
            <tr><td><b>{{field.label}} (at pH {{kow_ph}})</b></td>
            {% set skip = True %}
        {% elif field.html_name == "kow_ph" %}
            {% set skip = False %}
        {% else %}
            {% set skip = False %}
            <tr><td><b>{{field.label}}</b></td>
        {% endif %}
        {% if skip == False %}
            {% for prop, values in data.chemaxon.items %}
                {% if prop == field.label %}
                    <td>
                    {% for k,v in values.items %}
                        {{k}}:
                        {% for key, value in v.items %}
                            <i>{{value}}</i>
                        {% endfor %}
                        <br>
                    {% endfor %}
                    </td>
                {% endif %}
            {% endfor %}
        {% else %}
            {% for prop, values in data.chemaxon.items %}
                {% if prop == "Octanol/Water Partition Coefficient at pH" %}
                    <td>
                    {% for k,v in values.items %}
                        {{k}}:
                        {% for key, value in v.items %}
                            <i>{{value}}</i>
                        {% endfor %}
                        <br>
                    {% endfor %}
                    </td>
                {% endif %}
            {% endfor %}
        {% endif %}
        </tr>
    {% endfor %}
    </table>
    """
    return dj_template


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


pvuheadings = getheaderpvu()
structTmpl = Template(getStructInfoTemplate())
pchemTmpl = Template(getdjtemplate())


def table_all(pchemprop_obj):
    html_all = '<br>'
    html_all += input_struct_table(pchemprop_obj)
    html_all += output_pchem_table(pchemprop_obj)
    html_all += render_to_string('cts_display_raw_data.html', {'rawData': pchemprop_obj.rawData}) # temporary
    return html_all


def input_struct_table(pchemprop_obj):
    """
    structure information table (smiles, iupac, etc.)
    """

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section2"><span></span><b>Molecular Information</b></H4>
            <div class="out_ container_output">
    """
    t1data = getInputData(pchemprop_obj)
    t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + structTmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
    html = html + """
            </div>
    </div>
    """
    return html


def output_pchem_table(pchemprop_obj):
    """
    results of chemaxon properties 
    """
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>P-Chem Properties Results</H3>
    <div class="out_">
    """

    data = pchemprop_obj.resultsDict # get dict of pchemprop table - checked stuff
    
    allCalcsDict = {
        "chemaxon": None,
        "epi": None,
        "sparc": None,
        "test": None
    }

    kow_ph = round(float(pchemprop_obj.kow_ph), 1)
    pchemprops = pchemprop_parameters.cts_chemCalcs_props() # get pchemprop fields
    html += pchemTmpl.render(Context(dict(fields=pchemprops, data=data, kow_ph=kow_ph))) 

    html += """
    </div>
    """
    return html


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


