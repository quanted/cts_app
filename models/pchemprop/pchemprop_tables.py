
from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json
import pchemprop_parameters
from REST import webservice_map as wsMap


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


def getIonConDataChemaxon(pchemprop_obj):
    """
    Gets ionization constant data from results dict
    
    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with keys pKa and pKb, with
    values of [floats]
    
    TODO: Make more general for all calculators 
    """
    root = pchemprop_obj.resultsDict['chemaxon'] # root for getting ion con data
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


def getKowNoPhChemaxon(pchemprop_obj):
    """
    Gets octanol/water partition coefficient (logP)
    from results dict

    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with methodsListChemaxon keys (KLOP, VG, PHYS)
    and values of [logpnonionic]

    TODO: Make more general for all calculators
    """
    root = pchemprop_obj.resultsDict['chemaxon']
    kowNoPhResults = {key: [] for key in methodsListChemaxon} # methodsListChemaxon up top (KLOP, VG, PHYS)
    if root and 'kow_no_ph' in root:
        for method in methodsListChemaxon:
            try:
                root = pchemprop_obj.resultsDict['chemaxon']['kow_no_ph']
                value = round(root[method]['data'][0]['logP']['logpnonionic'], n)
                kowNoPhResults[method].append(value)
            except:
                kowNoPhResults[method].append("Exception getting logP...")
        return kowNoPhResults
    else:
        return None


def getKowWphChemaxon(pchemprop_obj):
    """
    Gets octanol/water partition coefficient with pH (logD)
    from results dict

    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with methodsListChemaxon keys (KLOP, VG, PHYS)
    and values of [logD]

    TODO: Make more general for all calculators
    """
    root = pchemprop_obj.resultsDict['chemaxon']
    kowWphResults = {key: [] for key in methodsListChemaxon}
    if root and 'kow_wph' in root:
        for method in methodsListChemaxon:
            try:
                root = pchemprop_obj.resultsDict['chemaxon']['kow_wph']
                root = root[method]['data'][0]['logD']

                phForLogD = float(pchemprop_obj.kow_ph) # convert to float
                chartDataList = root['chartData']['values'] # list of {"pH":val, "logD":val}

                for xyPair in chartDataList:
                  # use value at pH requested by user
                  if xyPair['pH'] == round(phForLogD, 1):
                      value = round(xyPair['logD'], n)
                      break

                kowWphResults[method].append(value)

            except:
                kowWphResults[method].append("Exception getting logD...")

        return kowWphResults
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
    """

    mainDataDict = {
        "chemaxon": {
            "ion_con": getIonConDataChemaxon(pchemprop_obj),
            "kow_no_ph": getKowNoPhChemaxon(pchemprop_obj),
            "kow_wph": getKowWphChemaxon(pchemprop_obj)
        },
        'test': pchemprop_obj.resultsDict['test'],
        'epi': pchemprop_obj.resultsDict['epi']
    }

    # for calc, calcData in pchemprop_obj.resultsDict.items():
    #     data = {} # prop -> data
    #     if calcData != None and calc != 'chemaxon':
    #         for prop, propData in calcData.items():
    #             data.update({prop: getPropDataFromCalc(calc, prop, propData, pchemprop_obj)})
    #         mainDataDict.update({calc: data}) 
        # elif calc != 'chemaxon':
        #     data.update({prop: getPropDataFromCalc(calc, None, calcData, None)})


    logging.info(" @@@ Main Data Dict: {} @@@ ".format(mainDataDict))

    kow_ph = 0.0
    if pchemprop_obj.kow_ph:
        kow_ph = round(float(pchemprop_obj.kow_ph), 1)

    html += render_to_string('cts_pchemprop_outputTable.html', 
                                { "data": mainDataDict, "kow_ph": kow_ph })
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


def getPropDataFromCalc(calc, prop, propData, pchemprop_obj):

    # logging.info("-{}-".format(propData))

    # TODO: Use webservice_map.py in REST or some other code-reuse way
    # instead of this "stunt"

    if calc == "chemaxon":
        if prop == "ion_con":
            return getIonConDataChemaxon(pchemprop_obj)
        elif prop == "kow_no_ph":
            return getKowNoPhChemaxon(pchemprop_obj)
        elif prop == "kow_wph":
            return getKowWphChemaxon(pchemprop_obj)

    elif calc == "test":
        # propData = json.loads(propData)
        # logging.info("TEST propData: {}, {}".format(prop, propData))
        testDict = {}
        for method in methodsListTEST:
            if prop == "melting_point":
                testDict.update({method: propData[method]})
                # testDict.update({method: propData['meltingPointTEST' + method]})
                # data.update({'meltingPointTESTFDA': propData['meltingPointTESTFDA']})
            elif prop == "boiling_point":
                testDict.update({method: propData[method]})
                # testDict.update({method: propData['boilingPointTEST' + method]})
                # data.update({'boilingPointTESTFDA': propData['boilingPointTESTFDA']})
            elif prop == "vapor_press":
                testDict.update({method: propData[method]})
                # testDict.update({method: propData['vaporPressureTEST' + method]})
                # data.update({'vaporPressureTESTFDA': propData['vaporPressureTESTFDA']})
            elif prop == "water_sol":
                testDict.update({method: propData[method]})
                # testDict.update({method: propData['waterSolubilityTEST' + method]})
                # data.update({'waterSolubilityTESTFDA': propData['waterSolubilityTESTFDA']})
            # elif prop == "kow_no_ph":
            #     data = propData['']

        # logging.info("TEST Dict: {}".format(testDict))

        return testDict

    elif calc == "epi":
        # propData = json.loads(propData)
        return propData[wsMap.calculator['epi']['props'][prop]]


# kowNoPhResults = {key: [] for key in methodsListChemaxon} # methodsListChemaxon up top (KLOP, VG, PHYS)
# if 'kow_no_ph' in pchemprop_obj.resultsDict['chemaxon']:
#     for method in methodsListChemaxon:
#         try:
#             root = pchemprop_obj.resultsDict['chemaxon']['kow_no_ph']
#             value = round(root[method]['data'][0]['logP']['logpnonionic'], n)
#             kowNoPhResults[method].append(value)
#         except:
#             kowNoPhResults[method].append("Exception getting logP...")
#     return kowNoPhResults
# else:
#     return None