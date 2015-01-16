
from django.template import Context, Template
import datetime
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import logging
import json
import pchemprop_parameters


# some constants:
methodsList = ["KLOP", "VG", "PHYS"] # method names used by some chemaxon properties
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


def getIonConData(pchemprop_obj):
    """
    Gets ionization constant data from results dict
    
    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with keys pKa and pKb, with
    values of [floats]
    
    TODO: Make more general for all calculators 
    """
    root = pchemprop_obj.resultsDict['chemaxon'] # root for getting ion con data
    logging.info(pchemprop_obj.resultsDict)
    ionConResults = { "ion_con": {"pKa": [], "pKb": [] } } # results dict for ion con
    if root and 'ion_con' in root:
        try:
            root = root['ion_con']['data'][0] # data root (most jchem data has this)
            for pka in root['pKa']['mostAcidic']:
                pka = round(float(pka), n)
                ionConResults["ion_con"]['pKa'].append(pka) # append to list at key pKa
            for pkb in root['pKa']['mostBasic']:
                pkb = round(float(pkb), n)
                ionConResults["ion_con"]['pKb'].append(pkb) # append to list at key pKb
        except:
            ionConResults["ion_con"]['pKa'].append("Exception getting pKa...")
            ionConResults["ion_con"]['pKb'].append("Exception getting pKb...")
        return ionConResults
    else:
        return None


def getKowNoPh(pchemprop_obj):
    """
    Gets octanol/water partition coefficient (logP)
    from results dict

    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with methodsList keys (KLOP, VG, PHYS)
    and values of [logpnonionic]

    TODO: Make more general for all calculators
    """
    kowNoPhResults = {'kow_no_ph': {key: [] for key in methodsList}} # methodsList up top (KLOP, VG, PHYS)
    if 'kow_no_ph' in pchemprop_obj.resultsDict['chemaxon']:
        for method in methodsList:
            try:
                root = pchemprop_obj.resultsDict['chemaxon']['kow_no_ph']
                value = round(root[method]['data'][0]['logP']['logpnonionic'], n)
                kowNoPhResults['kow_no_ph'][method].append(value)
            except:
                kowNoPhResults['kow_no_ph'][method].append("Exception getting logP...")
        return kowNoPhResults
    else:
        return None


def getKowWph(pchemprop_obj):
    """
    Gets octanol/water partition coefficient with pH (logD)
    from results dict

    Input: pchemprop_obj (see pchemprop_model)
    Returns: dictionary with methodsList keys (KLOP, VG, PHYS)
    and values of [logD]

    TODO: Make more general for all calculators
    """
    root = pchemprop_obj.resultsDict['chemaxon']
    kowWphResults = {'kow_wph': {key: [] for key in methodsList}}
    if 'kow_wph' in root:
        for method in methodsList:
            try:
                root = pchemprop_obj.resultsDict['chemaxon']['kow_wph']
                # value = root[method]['data'][0]['logD']['logD']
                root = root[method]['data'][0]['logD']

                phForLogD = float(pchemprop_obj.kow_ph) # convert to float
                chartDataList = root['chartData']['values'] # list of {"pH":val, "logD":val}

                for xyPair in chartDataList:
                  # use value at pH requested by user
                  if xyPair['pH'] == round(phForLogD, 1):
                      value = round(xyPair['logD'], n)
                      break

                kowWphResults['kow_wph'][method].append(value)

            except:
                kowWphResults['kow_wph'][method].append("Exception getting logD...")

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
# pchemTmpl = Template(getdjtemplate())
# tblTmpl = Template(getTableTemplate())


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
    <H3 class="out_1 collapsible" id="section1"><span></span>P-Chem Properties Results</H3>
    <div class="out_">
    """

    # Ionization Constant:
    ionConData = getIonConData(pchemprop_obj) # format: {"pKa": [floats], "pKb": [floats]}
    # Octanol/Water Partition Coefficient:
    kowNoPh = getKowNoPh(pchemprop_obj) # format: {"KLOP": [float], "VG": [float], "PHYS": [float]}
    # Octanal/Water Partition Coefficient at pH:
    kowWph = getKowWph(pchemprop_obj)

    # TODO: Make this less ugly, although it does work since there's only one key at 0th level
    data = {'chemaxon': {"ion_con": ionConData[ionConData.keys()[0]]}}
    data['chemaxon'].update({"kow_no_ph": kowNoPh[kowNoPh.keys()[0]]})
    data['chemaxon'].update({"kow_wph": kowWph[kowWph.keys()[0]]})
 
    kow_ph = round(float(pchemprop_obj.kow_ph), 1)

    html += render_to_string('cts_pchemprop_outputTable.html', 
                                { "data": data, "kow_ph": kow_ph })
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


