from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import redirect, render
import importlib
from .links_left import ordered_list
import logging
import os


#######################################################################################
################################ HTTP Error Pages #####################################
#######################################################################################

def generate_error_page(title=None, error_msg=None):
    """
    Generates error page to display to user if something went wrong.
    """
    html = render_to_string('01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        'TITLE': title,
        'TEXT_PARAGRAPH': error_msg
    })

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list(model='cts')  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    html += render_to_string('10epa_drupal_footer.html', {})

    return html



def fileNotFound(request, model=None):

	title = "File not found"
	error_msg = "The requested file/endpoint was not found."

	html = generate_error_page(title, error_msg)

	response = HttpResponse()
	response.write(html)
	return response



def requestTimeout(request):

	title = "Request timed out"
	error_msg = "The request has timed out. Please refresh the browser and try again."

	html = generate_error_page(title, error_msg)

	response = HttpResponse()
	response.write(html)

	return response


#######################################################################################
################################# Docs Redirect #######################################
#######################################################################################

def docsRedirect(request):
	return redirect('/docs/', permanent=True)
