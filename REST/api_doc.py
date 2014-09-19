from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import redirect
import importlib
# import linksLeft
import views.linksLeft
import logging



def doc(request):
    # html = render_to_string('01cts_uberheader.html', {'title': 'Error'})

    # html = html + render_to_string('02cts_uberintroblock_nomodellinks.html', {'title2':'Request timed out'})

    # html = html + views.linksLeft.linksLeft()

    # html = html + """<div class="articles"> 
    #                 <img class="model_header" src="/static/images/408error.png" width="300" height="300">
    #                 </div>"""

    # html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    # logging.warning("Inside of api_doc")

    text_file2 = open('REST/doc_text.txt','r')

    xx = text_file2.read()

    html = xx

    # html = render_to_string('04ubertext_start.html', {'text_paragraph':xx})

    # html = html + render_to_string('04ubertext_end.html')

    response = HttpResponse()
    response.write(html)

    return response    