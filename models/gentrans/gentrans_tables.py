"""
.. module:: gentrans_tables
   :synopsis: A useful module indeed.
"""
import datetime
import json
import os

from django.conf import settings
from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ..pchemprop import pchemprop_parameters


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


def getInputData(pchemprop_obj):
    data = [
        {'Entered chemical': pchemprop_obj.chem_struct},
        {'Standardized SMILES': pchemprop_obj.smiles},
        {'Initial SMILES': pchemprop_obj.orig_smiles},
        {'IUPAC': pchemprop_obj.iupac},
        {'Formula': pchemprop_obj.formula},
        {'Mass': pchemprop_obj.mass},
        {'Exact Mass': pchemprop_obj.exact_mass}
    ]
    return data


def getReactPathSimData(gentrans_obj):

    # Formats list of libraries used for display:
    libs = ""
    for item in gentrans_obj.trans_libs:
        libs += item + ", "
    libs = libs[:-2]

    data = [
        {'Libraries': libs},
        {'Generation Limit': gentrans_obj.gen_limit},
        # {'Population Limit': gentrans_obj.pop_limit},
        # {'Likely Limit': gentrans_obj.likely_limit}
    ]
    return data


tmpl = Template(getdjtemplate())
inTmpl = Template(getInputTemplate())


def table_all(gentrans_obj):

	html_all = table_inputs(gentrans_obj)
	
	html_all += '<script src="/static_qed/cts/js/scripts_pchemprop.js" type="text/javascript"></script>'
	html_all += render_to_string('cts_downloads.html', {'run_data': mark_safe(json.dumps(gentrans_obj.run_data))})
	html_all += table_metabolites(gentrans_obj)

	return html_all


def pchemprop_input_fields(gentrans_obj):
    """
    Fills hidden input element with
    pchemprop table inputs dictionary to
    be accessed on the front end for obtaining
    pchem props for selected metabolites
    """
    if hasattr(gentrans_obj, 'pchemprop_obj'):
        pchemprops = json.dumps(gentrans_obj.pchemprop_obj.__dict__)
        pchemprops_safe = ''
        for char in pchemprops:
            if char == '"':
                char = '&quot;'
            pchemprops_safe = pchemprops_safe + char
        html = '<input type="hidden" id="pchemprops" value="' + pchemprops_safe + '">'
        return html
    else:
        return ""


def table_inputs(gentrans_obj):
    html = """
    <br>
    <H3 class="out_1 collapsible" id="userInputs"><span></span>User Inputs</H3>
    <div class="out_">
    <table class="ctsTableStylin" id="inputsTable">
    """
    html += inTmpl.render(Context(dict(data=getInputData(gentrans_obj), heading="Molecular Information")))
    html += inTmpl.render(Context(dict(data=getReactPathSimData(gentrans_obj), heading="Reaction Pathway Simulator")))
    html += """
    </table>
    </div>
    <br>
    """
    return html


def timestamp(gentrans_obj="", batch_jid=""):
    if gentrans_obj:
        st = datetime.datetime.strptime(gentrans_obj.jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    else:
        st = datetime.datetime.strptime(batch_jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html="""
    <div class="out_" id="timestamp">
        <b>Generate Transformation Pathways<br>
    """
    html = html + st
    html = html + " (EST)</b>"
    html = html + """
    </div>"""
    return html


def table_metabolites(gentrans_obj):
	"""
	Populate input with hidden value
	of metabolites as a json string
	"""

	# new_result = ''
	# for char in gentrans_obj.results:
	# 	if char == '"':
	# 		char = '&quot;'
	# 	new_result = new_result + char

	# gentrans_obj.results = new_result

	# html = """
	# <H3 class="out_1 collapsible" id="reactionPathways"><span></span>Reaction Pathways</H3>
	# <div class="out_">
	# """
	# html += '<input id="hiddenJson" type="hidden" value="' + gentrans_obj.results + '">'
	html = build_pchem_table() # build pchem workflow's pchem table

	html += """
		<div id="cont">
		    <div id="center-cont">
		        <!-- the canvas container -->
		        <div id="infovis"></div>
		    </div>
		    <div id="log"></div>
		</div>
		<div id="reactionpathways">
		</div>
	"""

    # kow_ph = 7.4
    # if pchemprop_obj.kow_ph:
    #     kow_ph = round(float(pchemprop_obj.kow_ph), 1)

	html += render_to_string('cts_gentrans_tree.html', {'gen_max': gentrans_obj.gen_max})
	html += render_to_string('cts_pchemprop_requests.html', {
									"speciation_inputs": "null",
									"kow_ph": 7.0,
									"structure": mark_safe(gentrans_obj.smiles),
									"checkedCalcsAndProps": {},
									# "test_results": gentrans_obj.test_results,
									'nodes': 'null',
									'run_type': 'single',
									'workflow': 'gentrans',
									'nodejs_host': settings.NODEJS_HOST,
                                    'nodejs_port': settings.NODEJS_PORT,
                                    "iupac": mark_safe(gentrans_obj.iupac),
                                    "mass": gentrans_obj.mass,
                                    "formula": gentrans_obj.formula,
                                    'service': "getTransProducts",
                                    'metabolizer_post': mark_safe(json.dumps(gentrans_obj.metabolizer_request_post))
								}
							)


	# insert d3 test page template here:
	# html += render_to_string('d3_tree_test_page.html')


	html += """
	</div>
	"""

	return html


def build_pchem_table():
    """
    For window that displays metabolite's
    p-chem and structure data.
    """

    pchemHTML = render_to_string('cts_pchem.html', {})
    pchemHTML += str(pchemprop_parameters.form(None))  # recycling!

    html = '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'
    html += render_to_string('cts_gentrans_metabolites_nav.html', {'pchemHtml': pchemHTML})

    return html


def buildMetaboliteTableForPDF():
    # cts_pchem.html is pchem table, just remove checkbox inputs.
    # what other templates can be used??

    metTableTmpl = """

    {% for product in products %}
        <div class="metaboliteInfo">
            <div class="mol-info-wrapper">

                {{product.image}}

                <div class="nodeWrapDiv"></div>
                <table class="mol-info-table ctsTableStylin">
                    {% for key, val in product.items %}
                        {% if key in headings %}
                            <tr><td>{{key}}</td><td>{{val}}</td>
                        {% endif %}
                    {% endfor %}
                </table>

            </div>

            <br>

            <div class="pchem-wrapper">

                <table id="pchemprop_table" class="input_table">
                    <tr><td></td><td>ChemAxon</td><td>EPI Suite</td><td>TEST</td><td>SPARC</td><td>Measured</td></tr>

                    {% for data_row in product.data %}
                        <tr>
                        {% for row_item in data_row %}
                            <td>{{row_item}}</td>
                        {% endfor %}
                        </tr>
                    {% endfor %}

                </table>

            </div>
        </div>
        <br>
    {% endfor %}

    """
    return Template(metTableTmpl)