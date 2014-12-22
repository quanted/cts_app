"""
.. module:: chemspec_tables
   :synopsis: A useful module indeed.
"""

# import numpy
from django.template import Context, Template, defaultfilters
# from django.utils.safestring import mark_safe
# import logging
import time
import datetime
from django.template.loader import render_to_string
import logging
import json
from StringIO import StringIO
from django.utils.safestring import mark_safe
from models.gentrans import data_walks 


lgWidth = 250
mdWidth = 125 
smWidth = 75
scale = 100 


def getdjtemplate():
    dj_template ="""
    <dl class="shiftRight">
    {% for label, value in data.items %}
        <dd>
        {{label}}: {{value|default:"none"}}
        </dd>
    {% endfor %}
    </dl>
    """
    return dj_template


def getInputTemplate():
    input_template = """
    <th colspan="2" class="alignLeft">{{heading}}</th>
    {% for label, value in data.items %}
        <tr>
        <td>{{label}}</td> <td>{{value|default:"none"}}</td>
        </tr>
    {% endfor %}
    """
    return input_template


def getMolTblData(chemspec_obj):
    data = {
        'SMILES': chemspec_obj.smiles, 
        'IUPAC': chemspec_obj.name, 
        'Formula': chemspec_obj.formula, 
        'Mass': chemspec_obj.mass
    }
    return data


def getIsoPtData(chemspec_obj):
    data = {
        'Isoelectric Point': chemspec_obj.isoPtDict['isoPt']
    }
    return data


# Ionization Constants (pKa) Parameters Data
def getPkaInputs(chemspec_obj):
    data = {
        'Number of Decimals': chemspec_obj.pKa_decimals, 
        'pH Lower Limit': chemspec_obj.pKa_pH_lower, 
        'pH Upper Limit': chemspec_obj.pKa_pH_upper,  
        'pH Step Size': chemspec_obj.pKa_pH_increment,
        'Generate Major Microspecies at pH': chemspec_obj.pH_microspecies,
        'Isoelectric Point (pl) pH Step Size of Charge Distribution': chemspec_obj.isoelectricPoint_pH_increment
    }
    return data


# Dominate Tautomer Distribution Data
def getTautData(chemspec_obj):
    data = {
        'Maximum Number of Structures': chemspec_obj.tautomer_maxNoOfStructures, 
        'at pH': chemspec_obj.tautomer_pH
    }
    return data


# Stereoisomers Data
def getStereoData(chemspec_obj):
    data = {
        'Maximum Number of Structures': chemspec_obj.stereoisomers_maxNoOfStructures
    }
    return data


# Parent/Micro species data dictionary for templating
def getPkaValues(chemspec_obj):
    # jsonData = json.dumps(chemspec_obj.result)
    
    data = { 
        'Basic pKa Value(s)': chemspec_obj.pkaDict['mostBasicPka'], 
        'Acidic pKa Value(s)': chemspec_obj.pkaDict['mostAcidicPka']
    }
    return data


# djtemplate = getdjtemplate()
tmpl = Template(getdjtemplate())
inTmpl = Template(getInputTemplate())


def table_all(chemspec_obj):
    # html_all = '<script type="text/javascript" src="/static/stylesheets/structure_wrapper.js"></script>'
    html_all = '<script type="text/javascript" src="/static/stylesheets/qtip/jquery.qtip.js"></script>'
    html_all += '<link type="text/css" rel="stylesheet" href="/static/stylesheets/qtip/jquery.qtip.css"></link>'
    # inputs:
    html_all += table_inputs(chemspec_obj)
    # outputs:
    html_all += table_outputs(chemspec_obj)
    # raw data button and textbox:
    html_all += render_to_string('cts_display_raw_data.html', {'rawData': chemspec_obj.rawData}) # temporary
    # qtip popup script for images with class "wrapped_molecule"
    html_all += """
    <script>
    function tipit() {
        // Using qtip2 for tooltip
        $('.wrapped_molecule').each(function() {
            $(this).qtip({
                content: {
                    text: $(this).next('.tooltiptext')
                },
                style: {
                    classes: 'qtip-light'
                },
                position: {
                    my: 'bottom center',
                    at: 'center right',
                    target: 'mouse'
                }
            });
        });
    }
    </script>
    <script>
    tipit();
    </script>
    """
    return html_all


def timestamp(chemspec_obj="", batch_jid=""):
    if chemspec_obj:
        st = datetime.datetime.strptime(chemspec_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div>
        <b>Chemical Speciation - Version 1.0 (Alpha)<br>
    """
    html += st
    html += " (EST)</b>"
    html += """
    </div>"""
    return html


def table_inputs(chemspec_obj):
    """
    An attempt at making one large table
    for all user inputs. This will/would replace
    table_struct, table_pka_input, table_taut_input,
    and table_stereo_input
    """
    html = """
    <br>
    <H3 class="out_1 collapsible" id="section1"><span></span>User Inputs</H3>
    <div class="out_">
    <table id="chemspecInputs">
    """
    html += inTmpl.render(Context(dict(data=getMolTblData(chemspec_obj), heading="Molecular Information")))
    html += inTmpl.render(Context(dict(data=getPkaInputs(chemspec_obj), heading="Ionization Parameters")))
    html += inTmpl.render(Context(dict(data=getTautData(chemspec_obj), heading="Tautomer Parameters")))
    html += inTmpl.render(Context(dict(data=getStereoData(chemspec_obj), heading="Stereoisomer Parameters")))
    html += """
    </table>
    </div>
    """
    return html


def table_outputs(chemspec_obj):

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>Results</H3>
    <div class="out_">
    """
    # build output with below defs
    html += getPkaResults(chemspec_obj)
    html += getIsoPtResults(chemspec_obj)
    html += getMajorMsImages(chemspec_obj)
    html += table_stereo_results(chemspec_obj)
    html += table_taut_results(chemspec_obj)
    html += """
    </div>
    """
    return html


def getIsoPtResults(chemspec_obj):
    """
    IsoelectricPoint calculations
    """
    if chemspec_obj.isoPtDict:
        html = """
        <H4 class="out_1 collapsible" id="section6"><span></span>Isoelectric Point</H4>
        <div class="out_">
        """
        # isoelectric point value:
        tblData = getIsoPtData(chemspec_obj)
        ip = tblData['Isoelectric Point']
        # html += tmpl.render(Context(dict(data=tblData)))

        # isoelectric point plot:
        if 'isoPtChartData' in chemspec_obj.isoPtDict:
            html += '<div id="isoPtData" class="hideData">'
            html += mark_safe(json.dumps(chemspec_obj.isoPtDict['isoPtChartData']))
            html += '</div>'
            html += render_to_string('cts_plot_isoelectricPoint.html', {"ip": ip})
        html += """
        </div>
        """
        return html
    else:
        return ""


def getMajorMsImages(chemspec_obj):
    """
    MajorMicrospecies image
    """
    if chemspec_obj.majorMsDict:
        html = """
        <H4 class="out_1 collapsible" id="section6"><span></span>Major Microspecies</H4>
        <div class="out_ shiftRight">
        """
        html += wrap_molecule(chemspec_obj.majorMsDict, None, mdWidth, scale)
        html += """
        </div>
        """
        return html
    else:
        return ""


def getPkaResults(chemspec_obj):
    """
    pKa Calculations
    """
    if chemspec_obj.pkaDict:
        html = """
        <H4 class="out_1 collapsible" id="section6"><span></span>pKa</H4>
        <div class="out_">
        """

        # pKa acidic/basic values:
        tblData = getPkaValues(chemspec_obj)
        html += tmpl.render(Context(dict(data=tblData)))

        # pKa parent/microspecies images:
        html += """
        <table id="msMain">
        <tr>
        <td>
        """
        html += wrap_molecule(chemspec_obj.pkaDict['parent'], None, lgWidth, scale) + "<br>"
        html += """
        </td>
        <td>
        """
        if chemspec_obj.pkaDict['msImageUrlList']:
            for item in chemspec_obj.pkaDict['msImageUrlList']:
                html += wrap_molecule(item, None, smWidth, scale)
        else: 
            html += 'No microspecies to plot'
        html += """
        </td>
        <td>
        """

        # Microspecies Distribution Plot:
        if chemspec_obj.pkaDict['microDistData']:
            html += """
            <br>
            <div id="microDistData1" class="hideData">
            """
            html += mark_safe(json.dumps(chemspec_obj.pkaDict['microDistData']))
            html += '</div>'
            html += render_to_string('cts_plot_microspecies_dist.html')
        html += """
        </td>
        </table>
        </div>
        """
        return html
    else:
        return ""


def table_stereo_results(chemspec_obj):
    """
    Stereoisomers image 
    """
    if chemspec_obj.stereoDict:
        html = """
        <H4 class="out_1 collapsible" id="section10"><span></span>Stereoisomers</H4>
        <div class="out_ shiftRight">
        """
        html += wrap_molecule(chemspec_obj.stereoDict, None, mdWidth, scale)
        html += """
        </div>
        """
        return html
    else:
        return ""


def table_taut_results(chemspec_obj):
    """
    Tautomer image
    """
    if chemspec_obj.tautDict:
        html = """
        <H4 class="out_1 collapsible" id="section11"><span></span>Tautomerization</H4>
        <div class="out_ shiftRight">
        """
        html += '<dl style="display:inline-block">'
        for item in chemspec_obj.tautDict['tautStructs']:
            html += '<dd style="float:left;">' + wrap_molecule(item, None, mdWidth, scale) + '</dd>'
        html += "</dl>"
        html += """
        </div><br><br>
        """
        return html
    else:
        return ""


def wrap_molecule(propDict, height, width, scale):
    """
    Wraps molecule image result (source url) with a table
    and populates said table with molecular details.

    Inputs: property dict (e.g., pka, taut image urls)
    Outputs: name, iupac, forumula, mass data wrapped in table with image and name
    """

    key = None
    if 'key' in propDict:
        key = propDict['key']

    # image = propDict['image']
    # image = mark_safe(data_walks.nodeWrapper(propDict['smiles'], 114, 100, key)) # displayed image
    # image = mark_safe(data_walks.nodeWrapper(propDict['smiles'], height, width, key)) # displayed image
    image = mark_safe(data_walks.nodeWrapper(propDict['smiles'], None, width, scale, key)) # displayed image
    formula = propDict['formula']
    iupac = propDict['iupac']
    mass = propDict['mass']
    smiles = propDict['smiles']

    infoDict = {
        "image": image,
        "formula": formula,
        "iupac": iupac,
        "mass": mass,
        "smiles": smiles
    }

    # html = '<table class="' + defaultfilters.slugify(infoDict['iupac']) +' wrapped_molecule">'
    # # html += '<tr><td align="center">' + infoDict['iupac'] + '</td></tr>'
    # html += '<tr><td align="center">' + infoDict['image'] + '</td></tr></table>'

    html = """
    <div class="wrapped_molecule">
    """
    html += infoDict['image']
    html += """
    </div>
    """
    wrappedDict = data_walks.popupBuilder(infoDict, ['formula', 'iupac', 'mass', 'smiles'], key) # popup table image
    # html += '<div class="tooltiptext ' + iupac + '">' + wrappedDict['html'] + '</div>'
    html += '<div class="tooltiptext ' + iupac + '">'
    html += wrappedDict['html']
    html += '</div>'

    return html