
from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json
import pchemprop_parameters
from REST import calculator_map as calcMap


# some constants:
methodsListChemaxon = ["KLOP", "VG", "PHYS"] # method names used by some chemaxon properties
# methodsListTEST = ['FDA', 'Hierarchical', 'GroupContribution', 'Consensus', 'NearestNeighbor']
methodsListTEST = ['fda', 'hierarchical', 'group', 'consensus', 'neighbor']
n = 3 # number to round values to
headings = ["ChemAxon", "EPI Suite", "TEST", "SPARC", "Average"] # calulators 


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
        'SMILES': pchemprop_obj.smiles,
        'IUPAC': pchemprop_obj.name,
        'Formula': pchemprop_obj.formula,
        'Mass': pchemprop_obj.mass
    }
    return data


def getIonConDataChemaxon(chemaxonResultsDict):
    """
    Gets ionization constant data from results dict
    
    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with keys pKa and pKb, with
    values of [floats]
    
    TODO: Make more general for all calculators 
    """
    root = chemaxonResultsDict # root for getting ion con data
    ionConResults = {"pKa": [], "pKb": [] } # results dict for ion con
    if root and 'ion_con' in root:
        try:
            root = root['ion_con']['data'][0] # data root (most jchem data has this)
            for pka in root['pKa']['mostAcidic']:
                pka = round(float(pka), n)
                ionConResults['pKa'].append(pka)
            for pkb in root['pKa']['mostBasic']:
                pkb = round(float(pkb), n)
                ionConResults['pKb'].append(pkb)
        except:
            ionConResults['pKa'].append("Exception getting pKa...")
            ionConResults['pKb'].append("Exception getting pKb...")
        return ionConResults
    else:
        return None


def getKowNoPhChemaxon(chemaxonResultsDict):
    """
    Gets octanol/water partition coefficient (logP)
    from results dict

    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with methodsListChemaxon keys (KLOP, VG, PHYS)
    and values of [logpnonionic]

    TODO: Make more general for all calculators
    """
    root = chemaxonResultsDict
    kowNoPhResults = {key: [] for key in methodsListChemaxon} # methodsListChemaxon up top (KLOP, VG, PHYS)
    if root and 'kow_no_ph' in root:
        for method in methodsListChemaxon:
            try:
                root = chemaxonResultsDict['kow_no_ph']
                value = round(root[method]['data'][0]['logP']['logpnonionic'], n)
                kowNoPhResults[method].append(value)
            except:
                kowNoPhResults[method].append("Exception getting logP...")
        return kowNoPhResults
    else:
        return None


def getKowWphChemaxon(chemaxonResultsDict, kow_ph):
    """
    Gets octanol/water partition coefficient with pH (logD)
    from results dict

    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with methodsListChemaxon keys (KLOP, VG, PHYS)
    and values of [logD]

    TODO: Make more general for all calculators
    """
    root = chemaxonResultsDict
    kowWphResults = {key: [] for key in methodsListChemaxon}
    if root and 'kow_wph' in root:
        for method in methodsListChemaxon:
            try:
                root = chemaxonResultsDict['kow_wph']
                root = root[method]['data'][0]['logD']

                phForLogD = float(kow_ph) # convert to float
                chartDataList = root['chartData']['values'] # list of {"pH":val, "logD":val}

                for xyPair in chartDataList:
                  # use value at pH requested by user
                  if xyPair['pH'] == round(phForLogD, 1):
                      value = round(xyPair['logD'], n)
                      break

                kowWphResults[method].append(value)

            except KeyError:
                kowWphResults[method].append("Exception getting logD...")

        return kowWphResults
    else:
        return None


def getWaterSolChemaxon(chemaxonResultsDict):
    """
    Gets water solubility for chemaxon
    """
    root = chemaxonResultsDict
    waterSol = {}
    if root and 'water_sol' in root:
        try:
            root = chemaxonResultsDict['water_sol']
            value = round(1000.0 * root['data'][0]['solubility']['intrinsicSolubility'], n) # converted to mg/L
            return value
        except:
            return "Exception getting water solubility..."
    else:
        return None


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
    <table class="inputTableForOutput">
    <th colspan="2" class="alignLeft">{{heading}}</th>
    {% for label, value in data.items %}
        <tr>
        <td>{{label}}</td> <td>{{value|default:"none"}}</td>
        </tr>
    {% endfor %}
    </table>
    """
    return input_template


pvuheadings = getheaderpvu()
structTmpl = Template(getStructInfoTemplate())
inTmpl = Template(getInputTemplate())


def table_all(pchemprop_obj):
    html_all = '<br>'
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
    html = html + """
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

    <script type="text/javascript" src="/static/stylesheets/scripts_pchemprop_removeInputs.js"></script>
    """

    chemaxonDataDict = {}
    try:
        chemaxonResults = pchemprop_obj.chemaxonResultsDict
        chemaxonDataDict = {
            "ion_con": getIonConDataChemaxon(chemaxonResults),
            "kow_no_ph": getKowNoPhChemaxon(chemaxonResults),
            "kow_wph": getKowWphChemaxon(chemaxonResults, pchemprop_obj.kow_ph),
            "water_sol": getWaterSolChemaxon(chemaxonResults)
        }
    except AttributeError:
        pass

    kow_ph = 0.0
    if pchemprop_obj.kow_ph:
        kow_ph = round(float(pchemprop_obj.kow_ph), 1)

    # html += render_to_string('cts_pchemprop_outputTable.html', 
    #                             {   "chemaxonData": chemaxonDataDict, 
    #                                 "kow_ph": kow_ph, 
    #                                 "checkedCalcsAndProps": mark_safe(pchemprop_obj.checkedCalcsAndPropsDict) })

    pchemHTML = render_to_string('cts_pchem.html', {})
    pchemHTML += str(pchemprop_parameters.form(None))

    html += pchemHTML

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