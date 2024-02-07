"""
.. module:: chemspec_tables
   :synopsis: A useful module indeed.
"""
__author__ = 'np'

import datetime
import logging
import json
import os

from django.template import Context, Template, defaultfilters
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ...cts_calcs.calculator import Calculator
from ...cts_calcs.chemical_information import ChemInfo



# image sizes for jchem ws structures:
lgWidth = 250
mdWidth = 125 
smWidth = 75
scale = 100 # default is 28 

# cheminfo instance for building user-inputs table:
chem_info = ChemInfo()


def getdjtemplate():
    dj_template ="""
    <dl class="shiftRight" id="{{id|default:"none"}}" tabindex="0">
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
    {% for keyval in data %}
        {% for label, value in keyval.items %}
            <tr>
            <td>{{label}}</td> <td>{{value|default:"none"}}</td>
            </tr>
        {% endfor %}
    {% endfor %}
    """
    return input_template


def getIsoPtData(chemspec_obj):
    data = {
        'Isoelectric Point': chemspec_obj.isoPtDict['isoPt']
    }
    return data


# Ionization Constants (pKa) Parameters Data
def getPkaInputs(chemspec_obj):
    data = [
        {'Number of Decimals for pKa': chemspec_obj.pKa_decimals},
        {'pH Lower Limit': chemspec_obj.pKa_pH_lower}, 
        {'pH Upper Limit': chemspec_obj.pKa_pH_upper},  
        {'pH Step Size': chemspec_obj.pKa_pH_increment},
        {'Generate Major Microspecies at pH': chemspec_obj.pH_microspecies},
        {'Isoelectric Point (pI) pH Step Size of Charge Distribution': chemspec_obj.isoelectricPoint_pH_increment}
    ]
    return data


# Dominate Tautomer Distribution Data
def getTautData(chemspec_obj):
    data = [
        {'Maximum Number of Structures': chemspec_obj.tautomer_maxNoOfStructures}, 
        {'at pH': chemspec_obj.tautomer_pH}
    ]
    return data


# Stereoisomers Data
def getStereoData(chemspec_obj):
    data = [
        {'Maximum Number of Structures': chemspec_obj.stereoisomers_maxNoOfStructures}
    ]
    return data


# Parent/Micro species data dictionary for templating
def getPkaValues(chemspec_obj):
    data = { 
        'pKa Value(s)': chemspec_obj.pkaDict['mostAcidicPka']
    }
    return data


tmpl = Template(getdjtemplate())
inTmpl = Template(getInputTemplate())


def table_all(chemspec_obj):
    html_all = render_to_string('cts_app/cts_downloads.html', {'run_data': chemspec_obj.run_data})
    html_all += table_inputs(chemspec_obj)
    html_all += table_outputs(chemspec_obj)
    return html_all


def timestamp(chemspec_obj="", batch_jid=""):
    if chemspec_obj:
        st = datetime.datetime.strptime(chemspec_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div id="timestamp" class="out_">
        <b>Chemical Speciation<br>
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
    <H3 class="out_1 collapsible" id="userInputs"><span></span>User Inputs</H3>
    <div class="out_">
    <table class="ctsTableStylin" id="inputsTable" tabindex="0" aria-label="user inputs for {}">
    """.format(chemspec_obj.name)
    html += inTmpl.render(Context(dict(data=chem_info.create_cheminfo_table(chemspec_obj), heading="Molecular Information")))
    html += inTmpl.render(Context(dict(data=getPkaInputs(chemspec_obj), heading="Ionization Parameters")))
    html += inTmpl.render(Context(dict(data=getTautData(chemspec_obj), heading="Tautomer Parameters")))
    html += inTmpl.render(Context(dict(data=getStereoData(chemspec_obj), heading="Stereoisomer Parameters")))
    html += """
    </table>
    </div>
    <br>
    """
    return html


def table_outputs(chemspec_obj):

    html = """
    <H3 class="out_1 collapsible" id="section1"><span></span>Results</H3>
    <div class="out_">
    """
    html += getPkaResults(chemspec_obj)
    html += getIsoPtResults(chemspec_obj)
    html += getMajorMsImages(chemspec_obj)
    html += getStereoisomersResults(chemspec_obj)
    html += getTautomerResults(chemspec_obj)
    html += """
    </div>
    """
    return html


def getIsoPtResults(chemspec_obj):
    """
    IsoelectricPoint calculations
    """
    try:
        # isoPtObj = chemspec_obj.jchemPropObjects['isoelectricPoint']
        # isoPt = isoPtObj.getIsoelectricPoint()
        isoPt = chemspec_obj.run_data['isoelectricPoint']
        if isoPt:
            isoPt = round(isoPt, chemspec_obj.pKa_decimals)
        # isoPtChartData = isoPtObj.getChartData()
        isoPtChartData = chemspec_obj.run_data['isopt_chartdata']
    except Exception as e:
        logging.info("isoelectricPoint not checked..moving on..")
        return ""
    else:
        html = """
        <H4 class="out_1 collapsible" id="isoPt"><span></span>Isoelectric Point</H4>
        <div class="out_">
        """
        if isoPt:
            html += '<div id="isoPtData" class="hideData nopdf">'
            html += mark_safe(json.dumps(isoPtChartData))
            html += '</div>'
            html += render_to_string('cts_app/cts_plot_isoelectricPoint.html', {"ip": isoPt})
        else:
            html += '<p>No isoelectric point</p>'
        html += '</div>'
        return html


def getMajorMsImages(chemspec_obj):
    """
    MajorMicrospecies image
    """
    try:
        # majorMsDict = chemspec_obj.jchemPropObjects['majorMicrospecies'].getMajorMicrospecies()
        majorMsDict = chemspec_obj.run_data['majorMicrospecies']
    except Exception as e:
        logging.info("major microspecies not checked..moving on..")
        return ""
    else:
        html = """
        <H4 class="out_1 collapsible" id="majorMS"><span></span>Major Microspecies at pH: {}</H4>
        <div class="out_ shiftRight">""".format(chemspec_obj.pH_microspecies)
        html += wrap_molecule(majorMsDict, None, lgWidth, scale)
        html += """
        </div>
        """
        return html


def getPkaResults(chemspec_obj):
    html = """
    <H4 class="out_1 collapsible" id="pka"><span></span>pKa</H4>
    <div class="out_">
    """
    pkasolver_data = None

    try:
        # acidic/basic pKa values:
        pka = chemspec_obj.run_data['pka']
        pkb = chemspec_obj.run_data['pkb']
        roundedPka, roundedPkb = [], []
        for val in pka:
            roundedPka.append(round(val, chemspec_obj.pKa_decimals))
        for val in pkb:
            roundedPkb.append(round(val, chemspec_obj.pKa_decimals))

        pkasolver_data = chemspec_obj.run_data.get("pkasolver", {}).get("data", {})
        pkasolver_error = chemspec_obj.run_data.get("pkasolver", {}).get("error")

        logging.warning("pkasolver_data: {}".format(pkasolver_data))
        logging.warning("pkasolver_error: {}".format(pkasolver_error))

        # if chemspec_obj.run_data.get("pkasolver", {"data": {}}).get("data", {"pka_list": {}}).get("pka_list"):
        if pkasolver_data and pkasolver_data.get("pka_list"):
            pkasolver_val = pkasolver_data.get("pka_list")
        elif pkasolver_error:
            pkasolver_val = [pkasolver_error]
        else:
            pkasolver_val = ["Unknown error occurred with pkasolver."]

        logging.warning("pkasolver_val: {}".format(pkasolver_val))

        pkaValues = {
            'Acidic pKa Value(s)': roundedPka,
            'Basic pKa Value(s)': roundedPkb,
            'Pkasolver Values(s)': pkasolver_val
        }


    except Exception as e:
        logging.warning("no pka data.. moving on..\nException: {}".format(e))
        return ""
    else:
        html += tmpl.render(Context(dict(data=pkaValues, id="pkaValues")))

    # # Show/hide buttons for microspecies chart data:
    # html += """
    # <button id=btn-jchem onclick="toggleMicrospeciesTable('jchem')">Jchem</button>
    # <button id=btn-pkasolver onclick="toggleMicrospeciesTable('pkasolver')">Pkasolver</button>
    # """

    html += create_microspecies_tables(chemspec_obj, ['jchem', 'pkasolver'], pkasolver_data)  # TODO: generalize hardcoded list

    return html


# def create_microspecies_tables(chemspec_obj, chart_data, calc):
def create_microspecies_tables(chemspec_obj, calcs, pkasolver_data):
    """
    Builds microspecies table with parent, microspecies, and chart data.
    Will have options to view jchem or pkasolver data.
    """
    html = ""

    for calc in calcs:

        # TODO: Get these IDs for divs under control

        div_id = ""
        ms_div_name = calc + "-info"  # <div> id for calc MS info
        # html = ""
        chart_data = None
        microDistPlotId = None
        chart_data = None
        microspeciesList = None

        if calc == "pkasolver":

            if not pkasolver_data:
                continue
            
            html += """<button id=btn-pkasolver onclick="toggleMicrospeciesTable('pkasolver')">Pkasolver</button>"""
            
            chart_data = pkasolver_data.get('chart_data')
            microspeciesList = pkasolver_data.get('pka_microspecies')
            
            div_id = "microDistDataPkasolver"
            # html += '<div id="' + ms_div_name + '" style="display:none;">'  # defaults to hidden
            html += '<div id="' + ms_div_name + '">'  # defaults to shown

        elif calc == "jchem":
            
            html += """<button id=btn-jchem onclick="toggleMicrospeciesTable('jchem')">Jchem</button>"""
            
            chart_data = chemspec_obj.run_data['pka_chartdata']
            div_id = "microDistDataJchem"
            html += '<div id="' + ms_div_name + '">'  # defaults to shown

            microspeciesList = chemspec_obj.run_data['pka_microspecies']


        microDistPlotId = div_id + "Plot"

        # pKa parent species:
        html += '<table id="msMain" class="ctsTableStylin ' + calc + '"><tr><td><h4 class="unstyle">Parent</h4>'
        html += wrap_molecule(chemspec_obj.run_data['pka_parent'], None, lgWidth, scale)
        html += '<br></td><td id="ms-cell" class="' + calc + '"><h4 class="unstyle">Microspecies</h4>'

        try:
            for item in microspeciesList:
                html += wrap_molecule(item, None, mdWidth, scale)

        except TypeError as te:
            logging.info("no microspecies to plot..moving on")
            html += 'No microspecies to plot'

        html += '</td><td><br>'

        # Microspecies distribution plot data:
        html += '<div id=' + div_id + ' class="hideData nopdf">'
        if chart_data:
            html += mark_safe(json.dumps(chart_data))

        html += '</div>'

        # Chart div:
        html += """
        <div id="{}" class="plot microspecies-distribution" tabindex="0" aria-label="microspecies distribution"></div>
        """.format(microDistPlotId)

        html += '</td></table></div>'

        html += '</div>' 

    # One rendering for both chart data tables:
    html += render_to_string('cts_app/cts_plot_microspecies_dist.html',
        {
            'microDistCalcs': mark_safe(json.dumps({"calcs": calcs}))
        }
    )

    return html


def getStereoisomersResults(chemspec_obj):
    """
    Stereoisomers image 
    """
    try:
        # stereoList = chemspec_obj.jchemPropObjects['stereoisomers'].getStereoisomers()
        stereoList = chemspec_obj.run_data['stereoisomers']
    except Exception as e:
        logging.info("stereoisomers not checked..moving on..")
        return ""

    html = """
    <H4 class="out_1 collapsible" id="stereo"><span></span>Stereoisomers ({})</H4>
    """.format(len(stereoList))

    if stereoList:
        html += """
        <div class="out_ shiftRight">""".format(len(stereoList))
        
        html += '<dl style="display:inline-block">'
        for item in stereoList:
            html += '<dd style="float:left;">'
            html += wrap_molecule(item, None, lgWidth, scale)
            html += '</dd>'
        html += "</dl>"

        html += """
        </div>
        """
    else:
        html += """
        <p>Couldn't retrieve stereoisomer(s)..</p>
        """

    return html


def getTautomerResults(chemspec_obj):
    """
    Tautomer image
    """
    try:
        # tautStructs = chemspec_obj.jchemPropObjects['tautomerization'].getTautomers()
        tautStructs = chemspec_obj.run_data['tautomers']
    except Exception as e:
        logging.info("tautomerization not selected..moving on..")
        return ""

    html = """
    <H4 class="out_1 collapsible" id="taut"><span></span>Tautomerization (pH = 7.0)</H4>
    """

    if tautStructs:
        html += """
        <div class="out_ shiftRight">
        """
        html += '<dl style="display:inline-block">'
        for item in tautStructs:
            html += '<dd class="dom-taut" style="float:left;">'

            # MAJOR tautomer
            # if item:
            #     html += wrap_molecule(item, None, lgWidth, scale)
            # else:
            #     html += "No tautomers"

            # DOMINANT Tautomer:
            if item and 'dist' in item:
                html += '<p class="taut-percent" style="margin:0;">Percent Dist: {}%'.format(round(item['dist'], 2)) + "</p>"
                html += wrap_molecule(item, None, mdWidth, scale)
            else:
                html += "No tautomers"
                
            html += '</dd>'
        html += """
                </dl>
        </div>
        """
    else:
        html += """
        <p>Couldn't retrieve tautomer(s)..</p>
        """
    return html


def wrap_molecule(propDict, height, width, scale):
    """
    Wraps molecule image result (source url) with a table
    and populates said table with molecular details.

    Inputs: property dict (e.g., pka, taut image urls)
    Outputs: name, iupac, forumula, mass data wrapped in table with image and name
    """

    if not propDict:
        return "<p>could not retrieve molecule image</p>"

    key = None
    if 'key' in propDict:
        key = propDict['key']

    image = mark_safe(Calculator().nodeWrapper(propDict['smiles'], None, width, scale, key, 'svg')) # displayed image
    formula = propDict['formula']
    iupac = propDict['iupac']
    mass = "{} g/mol".format(propDict['mass'])
    smiles = propDict['smiles']
    exactMass = "{} g/mol".format(propDict['exactMass'])

    infoDict = {
        "image": image,
        "formula": formula,
        "iupac": iupac,
        "mass": mass,
        "smiles": smiles,
        "exactMass": exactMass
    }

    # this is the actual image on the chemspec output, wrapped in a div:
    html = """
    <div class="chemspec_molecule nopdf">
    """
    html += infoDict['image']
    html += """
    </div>
    """

    # the Molecular/Structure class/object needs to be used as well
    # as its location in CTS considered. Is it being in REST make sense?
    # the following list needs to be in that class:
    mol_props = ['formula', 'iupac', 'mass', 'smiles', 'exactMass']

    wrappedDict = Calculator().popupBuilder(infoDict, mol_props, key, 'Molecular Information') # popup table image
    html += '<div class="tooltiptext ' + iupac + '">'
    html += wrappedDict['html']
    html += '</div>'

    return html