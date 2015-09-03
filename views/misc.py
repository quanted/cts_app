from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import redirect, render
import importlib
import linksLeft
import logging


#######################################################################################
################################ HTTP Error Pages #####################################
#######################################################################################

def fileNotFound(request, model=None):
    html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
    html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2':'File not found'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04ubertext_start.html', {
            'model_attributes': 'This page is still under maintenance',
            'text_paragraph': ""})
    # html = html + """ <img src="/static/images/404error.png" width="300" height="300">"""
    html = html + """<img src="/static/images/fist-with-hammer.jpg" style="display:block; margin:auto;">"""
    html = html + render_to_string('04ubertext_end.html', {})
    html = html + render_to_string('05cts_ubertext_links_right.html', {})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)

    return response

def requestTimeout(request):
    html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
    html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2':'Request timed out'})
    html = html + linksLeft.linksLeft()
    # html = html + render_to_string('04ubertext_start.html', {
            # 'model_attributes': 'Request timed out',
            # 'text_paragraph': ""})
    html = html + """<div class="articles"> 
                    <img class="model_header" src="/static/images/408error.png" width="300" height="300">
                    </div>"""
    # html = html + render_to_string('04ubertext_end.html', {})
    html = html + render_to_string('05cts_ubertext_links_right.html', {})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)

    return response


def blankLanding(request, model=None):
    return render(request, 'blank_landing.html')


def displayPDF(request, reactionLib=None):

    if 'ahydrolysis' in request.path:
        logging.info('ahydrolysis in path!')
        title = 'Abiotic Hydrolysis Reaction Library'
        # pdfHTML = '<embed src="file_name.pdf" width=800px height=2100px>'
        pdfHTML = '<embed src="/static/docs/HydrolysisRxnLib_ver1-5.pdf" class="libPDF">'
    elif 'areduction' in request.path:
        logging.info('areduction in path!')
        title = 'Abiotic Reduction Reaction Library'
        pdfHTML = '<embed src="/static/docs/AbioticReductionRxnLib_vers1-4.pdf" class="libPDF">'
    else:
        logging.info('error')
        fileNotFound(request)
        return

    html = render_to_string('01cts_uberheader.html')
    html += render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2':'File not found'})
    html += linksLeft.linksLeft()
    html += render_to_string('04ubertext_start.html', {
            'model_attributes': title,
            'text_paragraph': "<br><br>"})
    html += pdfHTML
    # html = html + """<img src="/static/images/fist-with-hammer.jpg" style="display:block; margin:auto;">"""
    html += render_to_string('04ubertext_end.html', {})
    html += render_to_string('05cts_ubertext_links_right.html', {})
    html += render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)

    return response


def moduleDescription(request, module=None):

    logging.info("MODULE: " + module)

    html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
    html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2':'File not found'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04ubertext_start.html', {
            'model_attributes': 'This page is still under maintenance',
            'text_paragraph': ""})
    # html = html + """ <img src="/static/images/404error.png" width="300" height="300">"""
    html = html + """<img src="/static/images/fist-with-hammer.jpg" style="display:block; margin:auto;">"""
    html = html + render_to_string('04ubertext_end.html', {})
    html = html + render_to_string('05cts_ubertext_links_right.html', {})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)

    return response


#######################################################################################
################################# Docs Redirect #######################################
#######################################################################################

def docsRedirect(request):
    return redirect('/docs/', permanent=True)
