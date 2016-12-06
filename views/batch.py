from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
import linksLeft
import os
import logging
from models.pchemprop import pchemprop_tables
from cts_api import cts_rest
import datetime

def batchInputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    inputmodule = importlib.import_module('.'+model+'_batch', 'models.'+model)
    header = viewmodule.header
    
    html = render_to_string('01cts_uberheader.html', {'title': header+' Batch'})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'batchinput'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04uberbatchinput.html', {
            'model': model,
            'model_attributes': header+' Batch Run'})

    html += render_to_string('04uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js


    inputPageFunc = getattr(inputmodule, model+'BatchInputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    html = html + inputPageFunc(request, model, header)


    html = html + render_to_string('04uberbatchinput_jquery.html', {'model':model, 'header':header})
    
    # html = html + render_to_string('05cts_ubertext_links_right.html', {})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)
    return response

def batchOutputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    batchoutputmodule = importlib.import_module('.'+model+'_batch', 'models.'+model)
    header = viewmodule.header
    
    # linksleft = linksLeft.linksLeft()

    html = render_to_string('01cts_uberheader.html', {'title': header+' Batch'})
    # html += render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'batchinput'})
    html += render_to_string('02cts_uberintroblock_wmodellinks.html', 
        {'model':model,'page':'output'})
    html += linksLeft.linksLeft()

    html += render_to_string('04uberbatch_start.html', {
            'model': model,
            'model_attributes': header+' Batch Output'})

    # timestamp / version section
    st = datetime.datetime.strptime(cts_rest.gen_jid(), 
        '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html += """
    <div class="out_">
        <b>{} Batch Version 1.0</a> (Beta)<br>
    """.format(header)
    html += st
    html += " (EST)</b>"
    html += """
    </div><br><br>"""

    html = html + render_to_string('export.html', {})

    batchOutputPageFunc = getattr(batchoutputmodule, model+'BatchOutputPage')  # function name = 'model'BatchOutputPage  (e.g. 'sipBatchOutputPage')
    # batchOutputTuple = batchOutputPageFunc(request)

    # html = html + batchOutputTuple[0]

    html += batchOutputPageFunc(request)

    # html = html + render_to_string('export.html', {})
    html = html + render_to_string('04uberoutput_end.html', {})

    response = HttpResponse()
    response.write(html)
    return response