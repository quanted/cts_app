
from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json


def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getheaderpchem():
    headings = ["props", "klop","phys","vg", "weighted"]
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

def getChemaxonData(pchemprop_obj):
    data = {
        "Parameter": ['Ionization Constant:', 'Octanol/Water Partition Coefficient:', 'Octanol/Water Partition Coefficient at pH:'],
        "Value": [pchemprop_obj.chemaxonResultsDict['pKa'], pchemprop_obj.chemaxonResultsDict['logP'], pchemprop_obj.chemaxonResultsDict['logD']]
    }
    return data


def getPchempropData(calcDict):

    data = {
        "Property": calcDict['props'],
        "Value (KLOP)": calcDict['klop'],
        "Value (PHYS)": calcDict['phys'],
        "Value (VG)": calcDict['vg'],
        "Value (WEIGHTED)": calcDict['weighted']
    }
    return data


def template():
    template = """
    <table class="out_" id="">
        <tr>
        <th>Property</th>
        <th>Value (KLOP)</th>
        <th>Value (PHYS)</th>
        <th>Value (VG)</th>
        <th>Value (WEIGHTED)</th>
        </tr>
    </table>
    """
    return template


def getdjtemplate():
    dj_template ="""
    <table class="out_">
    {# headings #}
        <tr>
        {% for heading in headings %}
            <th>{{ heading }}</th>
        {% endfor %}
        </tr>
    {# data #}
    <tr>
    {% for item in data %}
    <td> {{item}} </td>
    {% endfor %}
    </tr>
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
# structInfoTemplate = getStructInfoTemplate()
structTmpl = Template(getStructInfoTemplate())
# pchemTemplate = getdjtemplate()
pchemTmpl = Template(getdjtemplate())


def table_all(pchemprop_obj):
    html_all = '<br>'
    html_all += input_struct_table(pchemprop_obj)
    html_all += output_chemaxon_table(pchemprop_obj)
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


def output_chemaxon_table(pchemprop_obj):
    """
    results of chemaxon properties 
    """
    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>P-Chem Properties Results</H3>
    <div class="out_">
        <H4 class="out_1 collapsible" id="section3"><span></span><b>Chemaxon Results</b></H4>
            <div class="out_ container_output">
    """

    # convert chemaxon dict to dict with keys: props, klop, phys, vg, weighted (all lists)

    data = pchemprop_obj.chemaxonResultsDict # get dict of pchemprop table - checked stuff

    propsList = []
    for key, value in data.items():
        dataDict = {}
        if key == 'pKa':
            dataDict.update({'props': "Ionization Constant"})
            ionConVal = {}
            for pKey, pVal in value.items():
                ionConVal.update({pKey: pVal})
            dataDict.update({'weighted': ionConVal})
            dataDict.update({'klop': ionConVal})
            dataDict.update({'phys': ionConVal})
            dataDict.update({'vg': ionConVal})
        if key == 'logP':
            dataDict.update({'props':"Octanol/Water Partition Coefficient"})
            logpVals = {
                "logP (nonionic)": value['logpnonionic'],
                "logD (pI)": value['logdpi']
            }
            dataDict.update({'weighted': logpVals})
            dataDict.update({'klop': logpVals})
            dataDict.update({'phys': logpVals})
            dataDict.update({'vg': logpVals})
        if key == 'logD':
            dataDict.update({'props': "Octanol/Water Partition Coefficient at pH"})
            logdVals = {"logD": value['logD']}
            dataDict.update({'weighted': logdVals})
            dataDict.update({'klop': logdVals})
            dataDict.update({'phys': logdVals})
            dataDict.update({'vg': logdVals})
        propsList.append(dataDict)

    # send to list to template
    # t1data = getInputData(pchemprop_obj)
    # t1rows = gethtmlrowsfromcols(dataDict, getheaderpchem())
    html += pchemTmpl.render(Context(dict(data=getPchempropData(dataDict), headings=getheaderpchem())))

    html += """
            </div>
    </div>
    """
    return html


def output_pKa_table(pchemprop_obj):
    """
    pKa results table
    """
    return None


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
