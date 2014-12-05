"""
.. module:: chemspec_tables
   :synopsis: A useful module indeed.
"""

# import numpy
from django.template import Context, Template
# from django.utils.safestring import mark_safe
# import logging
import time
import datetime
from django.template.loader import render_to_string
import logging
import json
# from PIL import Image
# import urllib2
from StringIO import StringIO

# logger = logging.getLogger("chemspecTables")

def getheaderpvu():
    headings = ["Parameter", "Value"]
    return headings

def getpkaheader():
    headings = ['Basic pKa Value(s)', 'Acidic pKa Value(s)']
    return headings

def getheaderspecies():
    headings = ["Parent Species", "Microspecies"]
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
    <table class="out_">
    {# headings #}
        <tr>
        {% for heading in headings %}
            <th>{{ heading }}</th>
        {% endfor %}
        </tr>
    {# data #}
    {% for row in data %}
    <tr>
        {% for val in row %}
        <td>{{ val|default:'' }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    </table>
    """
    return dj_template

def gett1data(chemspec_obj):
    data = { 
        "Parameter": ['Number of Decimals', 'pH Lower Limit', 'pH Upper Limit', 'pH Step Size','Generate Major Microspecies at pH', 'Isoelectric Point (pl) pH Step Size of Charge Distribution', 'Maximum Number of Structures', 'at pH', 'Maximum Number of Structures'],
        "Value": [chemspec_obj.pKa_decimals, chemspec_obj.pKa_pH_lower, chemspec_obj.pKa_pH_upper, chemspec_obj.pKa_pH_increment, chemspec_obj.pH_microspecies, chemspec_obj.isoelectricPoint_pH_increment, chemspec_obj.tautomer_maxNoOfStructures, chemspec_obj.tautomer_pH, chemspec_obj.stereoisomers_maxNoOfStructures],
    }
    return data

# Returned data from http://pnnl.cloudapp.net/efsws/chemproptest.html
def gett2data(chemspec_obj):
    data = { 
        "Parameter": ['Basic pKa Value(s)', 'Acidic pKa Value(s)'],
        "Value": [chemspec_obj.data[0]['pKa']['mostBasic'], chemspec_obj.data[0]['pKa']['mostAcidic']],
    }
    return data

# Parent/Micro species data dictionary for templating
def gett3data(chemspec_obj):
    # jsonData = json.dumps(chemspec_obj.result)

    # parentPath = str(chemspec_obj.result['image']['imageUrl']) # Image URL to parent chemical
    # parent_img = render_to_string('cts_display_image_test.html', {'path': parentPath})

    # plot = render_to_string('cts_plot_microspecies_dist.html')
    # logging.warning(plot)

    # Get paths of the microspecies:
    # microNum = len(chemspec_obj.microspecies)
    # micros = chemspec_obj.microspecies
    # microPaths = []

    # logging.warning(str(chemspec_obj))

    # html = ''

    # for i in range(0, microNum - 1):
    #     microPaths.append(str(micros[i]['image']['imageUrl']))

    #     # microPaths[i] = render_to_string('cts_display_image_test.html', {'path': microPaths[i]})
    #     html = html + render_to_string('cts_display_image_test.html', {'path': microPaths[i]})

    
    data = { 
        "Parameter": ['Basic pKa Value(s)', 'Acidic pKa Value(s)'],
        "Value": [chemspec_obj.data[0]['pKa']['mostBasic'], chemspec_obj.data[0]['pKa']['mostAcidic']],
    }


    return data


pvuheadings = getheaderpvu()
speciesheadings = getheaderspecies()
pkaheadings = getpkaheader()

djtemplate = getdjtemplate()
tmpl = Template(djtemplate)


def table_all(chemspec_obj):
    # html_all = render_to_string(timestamp)
    html_all = table_1(chemspec_obj)      
    # html_all = html_all + table_2(chemspec_obj)
    html_all = html_all + table_3(chemspec_obj)

    # html_all = html_all + render_to_string('cts_plot_microspecies_dist.html')

    return html_all

def timestamp(chemspec_obj="", batch_jid=""):
    if chemspec_obj:
        st = datetime.datetime.strptime(chemspec_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>Chemical Speciation - Version 1.0 (Alpha)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html


"""
User Inputs Table
"""
def table_1(chemspec_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
        """
        t1data = gett1data(chemspec_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        # t2data = gett2data(chemspec_obj)
        # t2rows = gethtmlrowsfromcols(t2data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        # html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
        </div>
        """
        return html


"""
Chemical Speciation Output (currently not used)
"""
# def table_2(chemspec_obj):
#         html = """
#         <br>
#         <H3 class="out_1 collapsible" id="section3"><span></span>Chemical Speciation Output</H3>
#         <div class="out_1">
#             <H4 class="out_1 collapsible" id="section4"><span></span>pKa Values</H4>
#                 <div class="out_ container_output">
#         """
#         t2data = gett2data(chemspec_obj)
#         t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
#         html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
#         html = html + """
#                 </div>
#         </div>
#         """
#         return html


"""
pKa Calculations Table
"""
def table_3(chemspec_obj):
        html = """
        <H3 class="out_1 collapsible" id="section3"><span></span>pKa Calculations</H3>
        <div class="out_1">
        """
        t3data = gett3data(chemspec_obj)
        t3rows = gethtmlrowsfromcols(t3data, pvuheadings)
        html = html + tmpl.render(Context(dict(data=t3rows, headings=pvuheadings)))
        html = html + """
        </div>
        """
        return html

