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
from ...cts_calcs.chemical_information import ChemInfo
from ..cts_pchem_definitions import pchem_defs



# cheminfo instance for building user-inputs table:
chem_info = ChemInfo()



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


def getReactPathSimData(gentrans_obj):

	# Formats list of libraries used for display:
	libs = ""
	for item in gentrans_obj.trans_libs:
		libs += item + ", "
	libs = libs[:-2]

	if not libs and gentrans_obj.calc == "metabolizer":
		# assume mammalian metabolism for now (may need revised when PFAS libs are introduced)
		libs = "mammalian_metabolism"
	elif not libs and gentrans_obj.calc == "biotrans":
		libs = "biotransformer_{}".format(gentrans_obj.biotrans_libs)
	elif not libs and gentrans_obj.calc == "envipath":
		libs = "microbial biotransformation"

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
	html_all += render_to_string('cts_downloads.html', {'run_data': gentrans_obj.run_data})
	html_all += table_metabolites(gentrans_obj)

	# Creates popup divs for p-chem table using qtip2 JS library:
	html_all += render_to_string('cts_pchem_definitions_popups.html', {'pchem_defs': pchem_defs})

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
	html += inTmpl.render(Context(dict(data=chem_info.create_cheminfo_table(gentrans_obj), heading="Molecular Information")))
	html += inTmpl.render(Context(dict(data=getReactPathSimData(gentrans_obj), heading="Reaction Pathway Simulator")))
	html += """
	</table>
	</div>
	<br>
	"""
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
				<div id="infovis" tabindex="0" aria-label="reaction pathway tree"></div>
			</div>
			<div id="log"></div>
			<div id="zoom-controls">
				<input id="zoom-out" class="zoom-buttons" type="button" value="-" aria-label="zoom out" />
				<input id="zoom-in" class="zoom-buttons" type="button" value="+" aria-label="zoom in" />
			</div>
		</div>
		<div id="reactionpathways">
		</div>
	"""

	# kow_ph = 7.4
	# if pchemprop_obj.kow_ph:
	#     kow_ph = round(float(pchemprop_obj.kow_ph), 1)

	html += render_to_string('cts_gentrans_tree.html', {'gen_max': gentrans_obj.gen_max})
	html += render_to_string('cts_pchemprop_requests.html',{
									"speciation_inputs": None,
									"kow_ph": 7.4,
									"structure": gentrans_obj.smiles,
									"orig_smiles": gentrans_obj.orig_smiles,
									"checkedCalcsAndProps": {},
									"calc": gentrans_obj.calc,
									'nodes': None,
									'run_type': 'single',
									'workflow': 'gentrans',
									'nodejs_host': settings.NODEJS_HOST,
									'nodejs_port': settings.NODEJS_PORT,
									"name": gentrans_obj.name,
									"mass": gentrans_obj.mass,
									"formula": gentrans_obj.formula,
									'service': "getTransProducts",
									'metabolizer_post': gentrans_obj.metabolizer_request_post,
									"include_rates": gentrans_obj.include_rates
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

	# html = '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'
	html = render_to_string('cts_gentrans_metabolites_nav.html', {'pchemHtml': pchemHTML})

	return html


def buildMetaboliteTableForPDF():
	# cts_pchem.html is pchem table, just remove checkbox inputs.
	# what other templates can be used??

	metTableTmpl = """

	{% for product in products %}
		<div class="metaboliteInfo">
			<div class="mol-info-wrapper">

				{{product.image|safe}}

				<div class="nodeWrapDiv"></div>
				<table class="mol-info-table ctsTableStylin">
					{% for heading in headings %}
						{% for key, val in product.items %}
							{% if key == heading %}
								<tr><td>{{key}}</td><td>{{val|default:"N/A"}}</td>
							{% endif %}
						{% endfor %}						
					{% endfor %}
				</table>

			</div>

			<br>

			{% if product.data %}

			<div class="pchem-wrapper">

				<table id="pchemprop_table" class="input_table">
				
					{% if sparc_available %}
					<tr><td></td><td>ChemAxon</td><td>EPI Suite</td><td>TEST</td><td>SPARC</td><td>Geometric Mean</td><td>Measured</td></tr>
					{% else %}
					<tr><td></td><td>ChemAxon</td><td>EPI Suite</td><td>TEST</td><td>Geometric Mean</td><td>Measured</td></tr>
					{% endif %}

					{% for data_row in product.data %}
					<tr>
					{% for row_item in data_row %}
						<td>{{row_item}}</td>
					{% endfor %}
					</tr>
					{% endfor %}

				</table>

			</div>

			{% endif %}


		</div>
		<br>
	{% endfor %}

	"""
	return Template(metTableTmpl)