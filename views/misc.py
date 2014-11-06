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

def fileNotFound(request):
    html = render_to_string('01cts_uberheader.html', {'title': 'Error'})
    html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2':'File not found'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04ubertext_start.html', {
            'model_attributes': 'File Not Found',
            'text_paragraph': ""})
    html = html + """ <img src="/static/images/404error.png" width="300" height="300">"""
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


def contact(request):
    return render(request, 'contact.html')


#######################################################################################
################################# Docs Redirect #######################################
#######################################################################################

def docsRedirect(request):
    return redirect('/docs/', permanent=True)
