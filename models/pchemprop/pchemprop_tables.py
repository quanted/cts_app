
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
        "Parameter": ['SMILES:', 'IUPAC:', 'Formula:', 'Mass:'],
        "Value": [pchemprop_obj.smiles, pchemprop_obj.name, pchemprop_obj.formula, pchemprop_obj.mass],
        # "Image": [pchemprop_obj.parentImage]
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
    ionConResults = { "Ionization Constant": {"pKa": [], "pKb": [] } } # results dict for ion con
    if root and 'Ionization Constant' in root:
        try:
            root = root['Ionization Constant']['data'][0] # data root (most jchem data has this)
            for pka in root['pKa']['mostAcidic']:
                ionConResults["Ionization Constant"]['pKa'].append(pka) # append to list at key pKa
            for pkb in root['pKa']['mostBasic']:
                ionConResults["Ionization Constant"]['pKb'].append(pkb) # append to list at key pKb
        except:
            ionConResults["Ionization Constant"]['pKa'].append("Exception getting pKa...")
            ionConResults["Ionization Constant"]['pKb'].append("Exception getting pKb...")
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
    kowNoPhResults = {'Octanol/Water Partition Coefficient': {key: [] for key in methodsList}} # methodsList up top (KLOP, VG, PHYS)
    if 'Octanol/Water Partition Coefficient' in pchemprop_obj.resultsDict['chemaxon']:
        for method in methodsList:
            try:
                root = pchemprop_obj.resultsDict['chemaxon']['Octanol/Water Partition Coefficient']
                value = round(root[method]['data'][0]['logP']['logpnonionic'], n)
                kowNoPhResults['Octanol/Water Partition Coefficient'][method].append(value)
            except:
                kowNoPhResults['Octanol/Water Partition Coefficient'][method].append("Exception getting logP...")
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
    kowWphResults = {'Octanol/Water Partition Coefficient at pH': {key: [] for key in methodsList}}
    if 'Octanol/Water Partition Coefficient at pH' in root:
        for method in methodsList:
            try:
                root = pchemprop_obj.resultsDict['chemaxon']['Octanol/Water Partition Coefficient at pH']
                # value = root[method]['data'][0]['logD']['logD']
                root = root[method]['data'][0]['logD']

                phForLogD = float(pchemprop_obj.kow_ph) # convert to float
                chartDataList = root['chartData']['values'] # list of {"pH":val, "logD":val}

                for xyPair in chartDataList:
                  # use value at pH requested by user
                  if xyPair['pH'] == round(phForLogD, 1):
                      value = round(xyPair['logD'], n)
                      break

                kowWphResults['Octanol/Water Partition Coefficient at pH'][method].append(value)

            except:
                kowWphResults['Octanol/Water Partition Coefficient at pH'][method].append("Exception getting logD...")

        return kowWphResults
    else:
        return None

# def getdjtemplate():
#     dj_template ="""
#     <table id="pchemprop_table_out" class="input_table tab tab_ChemCalcs">
#     <tr>
#         <th></th>
#         <th>ChemAxon</th>
#         <th>EPI Suite</th>
#         <th>TEST</th>
#         <th>SPARC</th>
#         <th>Measured</th>
#     </tr>

#     {% load set_var %}
#     {% set skip = False %}

#     {# loops through pchemprop_parameters fields #}
#     {% for field in fields %}
#         {# conditionals for appending kow_wph and kow_ph fields #}
#         {% if field.html_name == "kow_wph" %}
#             <tr><td><b>{{field.label}} (at pH {{kow_ph}})</b></td>
#             {% set skip = True %}
#         {% elif field.html_name == "kow_ph" %}
#             {% set skip = False %}
#         {% else %}
#             {% set skip = False %}
#             <tr><td><b>{{field.label}}</b></td>
#         {% endif %}
#         {% if skip == False %}
#             {% for prop, values in data.chemaxon.items %}
                # {% if prop == field.label %}
                #     <td>
                #     {% for k,v in values.items %}
                #         {{k}}:
                #         {% for key, value in v.items %}
                #             <i>{{value}}</i>
                #         {% endfor %}
                #         <br>
                #     {% endfor %}
                #     </td>
                # {% endif %}
#             {% endfor %}
#         {% else %}
#             {% for prop, values in data.chemaxon.items %}
#                 {% if prop == "Octanol/Water Partition Coefficient at pH" %}
#                     <td>
#                     {% for k,v in values.items %}
#                         {{k}}:
#                         {% for key, value in v.items %}
#                             <i>{{value}}</i>
#                         {% endfor %}
#                         <br>
#                     {% endfor %}
#                     </td>
#                 {% endif %}
#             {% endfor %}
#         {% endif %}
#         </tr>
#     {% endfor %}
#     </table>
#     """
#     return dj_template


def getTableTemplate():
    tblTmpl = """
    <table>

    <tr>
    <th></th>
    {% for heading in headings %}
        <th>{{heading}}</th>
    {% endfor %}
    </tr>

    {% load set_var %}
    {% set skip = False %}

    {# loops through pchemprop_parameters fields #}
    {% for field in props %}
        {# conditionals for appending kow_wph and kow_ph fields #}
        {% if field.html_name == "kow_wph" %}
            <tr><td><b>{{field.label}} at pH {{kow_ph}}</b></td>

            {% set skip = True %}
        {% elif field.html_name == "kow_ph" %}
            {% set skip = False %}
        {% else %}
            {% set skip = False %}
            <tr><td><b>{{field.label}}</b></td>
            {% for heading in headings %}
                <td>
                {% for calculator, values in data.items %}
                    {% if calculator == heading|slugify %}
                        {% for key, value in values.items %}
                            {% if key == field.label %}
                                {% for k,v in value.items %}
                                    <div style="float:left; text-align:center;">
                                    {% if k in methods %}
                                        <div>{{k}}</div>
                                        <div>{{v}}</div>
                                    {% endif %}
                                    </div>
                                {% endfor %}
                            {% endif %}
                        {% endfor %}
                    {% endif %}
                {% endfor %}
                </td>
            {% endfor %}
        {% endif %}
        </tr>
    {% endfor %}

    </table>
    """
    return tblTmpl


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
# pchemTmpl = Template(getdjtemplate())
tblTmpl = Template(getTableTemplate())


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

    # data = pchemprop_obj.resultsDict # get dict of pchemprop table - checked stuff

    # Ionization Constant:
    ionConData = getIonConData(pchemprop_obj) # format: {"pKa": [floats], "pKb": [floats]}
    # Octanol/Water Partition Coefficient:
    kowNoPh = getKowNoPh(pchemprop_obj) # format: {"KLOP": [float], "VG": [float], "PHYS": [float]}
    # Octanal/Water Partition Coefficient at pH:
    kowWph = getKowWph(pchemprop_obj)

    data = {}

    # TODO: Make this less ugly, although it does work since there's only one key at 0th level
    data.update({'chemaxon': {ionConData.keys()[0]: ionConData[ionConData.keys()[0]]}})
    data['chemaxon'].update({kowNoPh.keys()[0]: kowNoPh[kowNoPh.keys()[0]]})
    data['chemaxon'].update({kowWph.keys()[0]: kowWph[kowWph.keys()[0]]})

    logging.info("{}".format(data))
 
    kow_ph = round(float(pchemprop_obj.kow_ph), 1)
    pchemprops = pchemprop_parameters.cts_chemCalcs_props() # get pchemprop fields
    # html += pchemTmpl.render(Context(dict(fields=pchemprops, data=data, kow_ph=kow_ph, headings=headings))) 
    
    # html += '<table>'
    # html += tblTmpl.render(Context(dict(headings=headings)))
    html += tblTmpl.render(Context(dict(headings=headings, props=pchemprops, kow_ph=kow_ph, data=data, methods=methodsList)))

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


