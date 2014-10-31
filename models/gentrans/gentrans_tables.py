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

def getInputData(gentrans_obj):
    data = { 
        "Parameter": ['chemical', 'library', 'generation limit', 'population limit', 'likely limit'],
        "Value": [gentrans_obj.chem_struct, gentrans_obj.trans_libs, gentrans_obj.gen_limit, gentrans_obj.pop_limit, gentrans_obj.likely_limit]
    }
    return data


# def gett2data(gentrans_obj):
#     data = { 
#         "Parameter": ['Basic pKa Value(s)', 'Acidic pKa Value(s)'],
#         "Value": [gentrans_obj.basicpKaValues, gentrans_obj.acidicpKaValues],
#         "Units": [''],
#     }
#     return data


pvuheadings = getheaderpvu()
pvrheadings = getheaderpvr()
# pvrheadingsqaqc = getheaderpvrqaqc()
# sumheadings = getheadersum()
djtemplate = getdjtemplate()
tmpl = Template(djtemplate)

def table_all(gentrans_obj):
    # html_all = render_to_string(timestamp)
    # html_all = table_1(gentrans_obj)

    html_all = table_metabolites(gentrans_obj)

    html_all = html_all + """
    <input type="button" onclick="init();" value="show tree">
    <div id="cont">
    <div id="center-cont">
        <!-- the canvas container -->
        <div id="infovis"></div>    
    </div>
    <div id="log"></div>
    </div>
    """

    # html_all = html_all = '<div id="degrade"></div>'  

    # html_all = html_all + '<input type="hidden" id="jsonResult" value="' + str(gentrans_obj.results) + '">'


    # html_all = html_all + table_2(gentrans_obj)<%=Response.HTMLEncode(strQ)%>">
    #html_all = html_all + table_3(gentrans_obj)
    return html_all

def timestamp(gentrans_obj="", batch_jid=""):
    if gentrans_obj:
        st = datetime.datetime.strptime(gentrans_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_">
        <b>SIP <a href="http://www.epa.gov/oppefed1/models/terrestrial/sip/sip_user_guide.html">Version 1.0</a> (Beta)<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html

def table_1(gentrans_obj):
        html = """
        <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
        <div class="out_">
            <H4 class="out_1 collapsible" id="section2"><span></span>Application and Chemical Information</H4>
                <div class="out_ container_output">
        """
        t1data = getInputData(gentrans_obj)
        t1rows = gethtmlrowsfromcols(t1data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t1rows, headings=pvuheadings)))
        html = html + """
                </div>
        </div>
        """
        return html


def table_2(gentrans_obj):
        html = """
        <br>
        <H3 class="out_1 collapsible" id="section3"><span></span>Chemical Speciation Output</H3>
        <div class="out_1">
            <H4 class="out_1 collapsible" id="section4"><span></span>pKa Values</H4>
                <div class="out_ container_output">
        """
        t2data = gett2data(gentrans_obj)
        t2rows = gethtmlrowsfromcols(t2data,pvuheadings)
        html = html + tmpl.render(Context(dict(data=t2rows, headings=pvuheadings)))
        html = html + """
                </div>
        """
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

    html = '<input id="hiddenJson" type="hidden" value="' + gentrans_obj.results + '">'

    return html


