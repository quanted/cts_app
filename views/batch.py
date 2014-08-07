from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
import linksLeft

import logging

def batchInputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    header = viewmodule.header
    
    html = render_to_string('01cts_uberheader.html', {'title': header+' Batch'})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'batchinput'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04uberbatchinput.html', {
            'model': model,
            'model_attributes': header+' Batch Run'})
    if model == 'przm':
        html = html + render_to_string('04uberbatchinput_jquery_przm_batch.html', {'model':model, 'header':header})
    else:
        html = html + render_to_string('04uberbatchinput_jquery.html', {'model':model, 'header':header})
    html = html + render_to_string('05cts_ubertext_links_right.html', {})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)
    return response

def batchOutputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    batchoutputmodule = importlib.import_module('.'+model+'_batchoutput', 'models.'+model)
    from REST import rest_funcs
    header = viewmodule.header
    linksleft = linksLeft.linksLeft()

    html = render_to_string('04uberbatch_start.html', {
            'model': model,
            'model_attributes': header+' Batch Output'})

    batchOutputPageFunc = getattr(batchoutputmodule, model+'BatchOutputPage')  # function name = 'model'BatchOutputPage  (e.g. 'sipBatchOutputPage')
    batchOutputTuple = batchOutputPageFunc(request)
    if model == 'przm':
        logging.info(batchOutputTuple)
        html = html + ''
    else:
        html = html + batchOutputTuple[0]
        html = html + render_to_string('export.html', {})
        html = html + render_to_string('04uberoutput_end.html', {})

        model_all = batchOutputTuple[1]
        jid_batch = batchOutputTuple[2]
        rest_funcs.batch_save_dic(html, [x.__dict__ for x in model_all], model, 'batch', jid_batch[0], linksleft)

    response = HttpResponse()
    response.write(html)
    return response