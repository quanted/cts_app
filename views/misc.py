from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import redirect, render
import importlib
from .linksLeft import linksLeft
import logging
import os


#######################################################################################
################################ HTTP Error Pages #####################################
#######################################################################################

def fileNotFound(request, model=None):
	html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
	html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2': 'File not found'})
	html = html + linksLeft.linksLeft()
	html = html + render_to_string('04ubertext_start.html', {
		'model_attributes': 'This page is still under maintenance',
		'text_paragraph': ""})
	# html = html + """ <img src="/static_qed/cts/images/404error.png" width="300" height="300">"""
	html = html + """<img src="/static_qed/cts/images/fist-with-hammer.jpg" style="display:block; margin:auto;">"""
	html = html + render_to_string('04cts_ubertext_end.html', {})
	# html = html + render_to_string('05cts_ubertext_links_right.html', {})
	html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
	response = HttpResponse()
	response.write(html)
	return response


def requestTimeout(request):
	html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
	html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2': 'Request timed out'})
	html = html + linksLeft.linksLeft()
	html = html + """<div class="articles">
                    <img class="model_header" src="/static_qed/cts/images/408error.png" width="300" height="300">
                    </div>"""
	# html = html + render_to_string('05cts_ubertext_links_right.html', {})
	html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

	response = HttpResponse()
	response.write(html)

	return response


# def displayPDF(request, reactionLib=None):
# 	if 'ahydrolysis' in request.path:
# 		logging.info('ahydrolysis in path!')
# 		title = 'Abiotic Hydrolysis Reaction Library'
# 		# pdfHTML = '<embed src="file_name.pdf" width=800px height=2100px>'
# 		pdfHTML = """
# 		<p>Version 1.6 of the Abiotic Hydrolysis Reaction Library contains 25 reaction schemes.  Left click a reaction scheme to view the generalized reaction scheme, supporting reaction rules for reactivity, selectivity and exclusion, as well as example transformation pathways based on the execution of the reaction scheme.  References to process science on which the reaction scheme was developed are also provided.</p>
# 		<br>
# 		<h3> Click <a href="/static_qed/cts/docs/HydrolysisRxnLib_ver1-6.pdf" download="HydrolysisRxnLib_ver1-6.pdf">here</a> to download if file doesn't load</h3>
# 		<embed src="/static_qed/cts/docs/HydrolysisRxnLib_ver1-6.pdf" class="libPDF">
# 		"""
# 	elif 'areduction' in request.path:
# 		logging.info('areduction in path!')
# 		title = 'Abiotic Reduction Reaction Library'
# 		pdfHTML = """
# 		<p>Version 1.4 of the Abiotic Reduction Reaction Library contains 8 reaction schemes.  Left click a reaction scheme to view the generalized reaction scheme, supporting reaction rules for reactivity, selectivity and exclusion, as well as example transformation pathways based on the execution of the reaction scheme.  References to process science on which the reaction scheme was developed are also provided.</p>
# 		<br>
# 		<h3> Click <a href="/static_qed/cts/docs/AbioticReductionRxnLib_vers1-4.pdf" download="AbioticReductionRxnLib_vers1-4.pdf">here</a> to download if file doesn't load</h3>
# 		<embed src="/static_qed/cts/docs/AbioticReductionRxnLib_vers1-4.pdf" class="libPDF">
# 		"""
# 	# elif 'guide' in request.path:
# 	# 	title = "CTS User's Guide"
# 	# 	pdfHTML = """
# 	# 	<h3> Click <a href="/static_qed/cts/docs/CTS_USER_Guide_weber_9-14-15.docx" download="CTS_USER_Guide_weber_9-14-15.docx">here</a> to download if the file does not load </h3>
# 	# 	<embed src="/static_qed/cts/docs/CTS_USER_Guide_weber_9-14-15.docx" class="libPDF">'
# 	# 	"""
# 	else:
# 		logging.info('error')
# 		return fileNotFound(request)

# 	html = render_to_string('01cts_uberheader.html')
# 	html += render_to_string('02cts_uberintroblock_nomodellinks.html')
# 	html += linksLeft.linksLeft()
# 	html += render_to_string('04ubertext_start.html', {
# 		'model_attributes': title,
# 		'text_paragraph': pdfHTML})
# 		# 'text_paragraph': "<br><br>"})
# 	# html += pdfHTML
# 	# html = html + """<img src="/static_qed/cts/images/fist-with-hammer.jpg" style="display:block; margin:auto;">"""
# 	html += render_to_string('04cts_ubertext_end.html', {})
# 	html += render_to_string('05cts_ubertext_links_right.html', {})
# 	html += render_to_string('06cts_uberfooter.html', {'links': ''})

# 	response = HttpResponse()
# 	response.write(html)

# 	return response


# def moduleDescriptions(request, module=None):
# 	logging.info("MODULE: " + module)

# 	html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
# 	html += render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2': 'File not found'})
# 	html += linksLeft.linksLeft()

# 	module_text = ""
# 	if module == 'chemedit-description':
# 		module_text = chemeditDescription()
# 	elif module == 'pchemprop-description':
# 		module_text = pchempropDescription()
# 	elif module == 'reactsim-description':
# 		module_text = reactsimDescription()
# 	elif module == 'mamm-metabo':
# 		module_text = mMetabolismDescription()

# 	# body of page:
# 	html += render_to_string('04ubertext_start.html', {
# 		'model_attributes': "",
# 		'text_paragraph': module_text
# 	})
	
# 	html += render_to_string('04cts_ubertext_end.html', {})
# 	html += render_to_string('05cts_ubertext_links_right.html', {})
# 	html += render_to_string('06cts_uberfooter.html', {'links': ''})

# 	response = HttpResponse()
# 	response.write(html)

# 	return response


# def chemeditDescription():
# 	html = """
#         <p><b>Chemical Editor (CE):</b> Provides options for chemical entry by entering a SMILES string, IUPAC name, CAS#, or by drawing a structure for the chemical of interest.  Through the execution of the Calculate Chemical Speciation Workflow, the chemical speciation of a chemical, which includes the calculation of ionization constants, the dominant tautomer distribution, as well as structures for all possible isomers, can be calculated/generated. </p>
#         """
# 	return html


# def pchempropDescription():
# 	html = """
#     <p><b>Physicochemical Properties (PCP): </b> Calculates physicochemical properties for the parent chemical and predicted transformation products based on the executions of multiple p-chem calculators.  The PCP is based on a consensus approach that would allow the user to compare output generated by a number of calculators that take different approaches to calculating specific physicochemical properties.  The calculators we are currently accessing include (1) SPARC (SPARC Performs Automated Reasoning in Chemistry), which uses a mechanistic-based approach, (2) EPI Suite, which uses a fragment-based approach, (3) TEST (Toxicity Estimation Software Tool), which uses QSAR-based approaches, and (4) ChemAxon plug-in calculators, which use an atom-based fragment approach.  The user also has the option to request measured data that is available in the EPI Suite p-chem database.  </p>
#     """
# 	return html


# def reactsimDescription():
# 	# this could be a template as well, but currently not necessary
# 	html = """
#     <p><b>Reaction Pathway Simulator (RPS)</b>: Generates potential transformation products based on user-specified reaction conditions. The output of the RPS is based on the selection and execution of reaction libraries that represent reaction schemes for the transformation of reactive functional groups (i.e., reduction and hydrolysis). These reaction schemes represent viable transformation pathways based on the identification and subsequent transformation of the reactive functional groups. A reaction library for human metabolism for phase 1 transformations developed by ChemAxon is also available through the RPS. The development of reaction libraries allow us to "encode" the known process science published (current and future) in the peer-reviewed literature. The encoding of process science is accomplished through the use of Chemical Terms Language and cheminformatics applications. The execution of these reaction libraries provides dominant transformation pathways and products for the chemical of interest as a function of environmental conditions. The user also has the option to execute the PCP module for the calculation of physicochemical properties for the parent chemical and transformation products.</p>
#     """
# 	return html


# def mMetabolismDescription():
# 	html = """
# 	The Human Phase 1 Reaction Library contains 156 reaction schemes based on CYP450 Phase 1 biotransformations. This reaction library was developed by Chemaxon. The reaction library is proprietary, and thus, details of the reactions schemes cannot be viewed.
# 	"""
# 	return html


#######################################################################################
################################# Docs Redirect #######################################
#######################################################################################

def docsRedirect(request):
	return redirect('/docs/', permanent=True)
