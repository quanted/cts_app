"""
.. module:: gentrans_tables
   :synopsis: A useful module indeed.
"""

# import numpy
from django.template import Context, Template
# from django.utils.safestring import mark_safe
# import logging
# import time
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json

from models.pchemprop import pchemprop_tables
# import importlib
import gentrans_output

# logger = logging.getLogger("gentransTables")

def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpvr():
	headings = ["Parameter", "Acute", "Chronic","Units"]
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


def getdjtemplate():
    dj_template ="""
    <dl class="shiftRight">
    {% for label, value in data.items %}
        <dd>
        <b>{{label}}:</b> {{value|default:"none"}}
        </dd>
    {% endfor %}    
    </dl>
    """
    return dj_template


def getStructInfo(gentrans_obj):
    data = {
        'SMILES': gentrans_obj.smiles, 
        'IUPAC': gentrans_obj.name, 
        'Formula': gentrans_obj.formula, 
        'Mass': gentrans_obj.mass
    }
    return data


def getReactPathSimData(gentrans_obj):
    data = { 
        'Libraries': gentrans_obj.trans_libs, 
        'Generation Limit': gentrans_obj.gen_limit, 
        'Population Limit': gentrans_obj.pop_limit, 
        'Likely Limit': gentrans_obj.likely_limit
    }
    return data


pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_all(gentrans_obj):
    html_all = '<br>'
    html_all += table_struct(gentrans_obj)
    html_all += table_reactPathSim(gentrans_obj)
    # html_all += table_pchemprops()
    html_all += table_metabolites(gentrans_obj)
    html_all += render_to_string('cts_display_raw_data.html', {'rawData': gentrans_obj.rawData})
    return html_all


def timestamp(gentrans_obj="", batch_jid=""):
    if gentrans_obj:
        st = datetime.datetime.strptime(gentrans_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
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


def table_struct(gentrans_obj):
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section4"><span></span><b>Molecular Information</b></H4>
            <div class="out_ container_output">
    """
    tblData = getStructInfo(gentrans_obj)
    # t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=tblData)))
    html = html + """
            </div>
    """
    return html


def table_reactPathSim(gentrans_obj):
    html = """
        <H4 class="out_1 collapsible" id="section4"><span></span><b>Reaction Pathway Simulator</b></H4>
            <div class="out_ container_output">
    """
    tblData = getReactPathSimData(gentrans_obj)
    # t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
    html = html + tmpl.render(Context(dict(data=tblData)))
    html = html + """
            </div>
    """
    return html


def table_pchemprops():
    # html = """
    #     <H4 class="out_1 collapsible" id="section4"><span></span><b>P-Chem Properties Results</b></H4>
    #         <div class="out_ container_output">
    # """
    model_obj = gentrans_output.gentransOutputPage.pchemprop_obj 
    html = pchemprop_tables.output_pchem_table(model_obj)
    # html += """
    #         </div>
    # </div>
    # """
    return html
    


"""
Populate input with hidden value
of metabolites as a json string
"""
def table_metabolites(gentrans_obj):

    new_result = ''
    for char in gentrans_obj.results:
        if char == '"':
            char = '&quot;'
        new_result = new_result + char

    gentrans_obj.results = new_result

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>Reaction Pathways</H3>
    <div class="out_">
    """
    html += '<input id="hiddenJson" type="hidden" value="' + gentrans_obj.results + '">'
    html += render_to_string('cts_gentrans_tree.html')
    html += """
    </div>
    """

    return html


