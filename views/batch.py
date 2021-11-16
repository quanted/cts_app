import importlib
import datetime
import os
import logging
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from .links_left import ordered_list
from cts_app.models.pchemprop import pchemprop_tables
# from cts_app.cts_api import cts_rest
from ..cts_calcs.calculator import Calculator


@requires_csrf_token
def batchInputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    inputmodule = importlib.import_module('.'+model+'_batch', 'cts_app.models.'+model)
    header = viewmodule.header

    #drupal template for header with bluestripe
    html = render_to_string('cts_app/01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })

    html += render_to_string('cts_app/02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('cts_app/03epa_drupal_section_title_cts.html', {"version": os.getenv("CTS_VERSION")})

    html += render_to_string('cts_app/06cts_ubertext_start_index_drupal.html', {
        # 'TITLE': 'Calculate Chemical Speciation',
        # 'TEXT_PARAGRAPH': xx
    })


    html = html + render_to_string('cts_app/04cts_uberbatchinput.html', {
            'model': model,
            'model_attributes': header+' Batch Run'}, request=request)
    html += render_to_string('cts_app/04cts_uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js
    inputPageFunc = getattr(inputmodule, model+'BatchInputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    html = html + inputPageFunc(request, model, header)

    html = html + render_to_string('cts_app/04cts_uberbatchinput_jquery.html',
        {
            'model':model,
            'header':header,
            'nodejsHost': settings.NODEJS_HOST,
            'nodejsPort': settings.NODEJS_PORT
        })


    html += render_to_string('cts_app/07ubertext_end_drupal.html', {})
    # html += links_left.ordered_list(model='cts/' + model)  # fills out 05ubertext_links_left_drupal.html
    html += ordered_list(model='cts/' + model, page='batch')

    #scripts and footer
    html += render_to_string('cts_app/09epa_drupal_ubertool_css.html', {})
    html += render_to_string('cts_app/09epa_drupal_cts_css.html')
    html += render_to_string('cts_app/09epa_drupal_cts_scripts.html', request=request)
    #html += render_to_string('cts_app/09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('cts_app/10epa_drupal_footer.html', {})


    response = HttpResponse()
    response.write(html)
    return response


@requires_csrf_token
def batchOutputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    batchoutputmodule = importlib.import_module('.'+model+'_batch', 'cts_app.models.'+model)
    header = viewmodule.header
    


    #drupal template for header with bluestripe
    html = render_to_string('cts_app/01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })

    html += render_to_string('cts_app/02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('cts_app/03epa_drupal_section_title_cts.html', {"version": os.getenv("CTS_VERSION")})

    html += render_to_string('cts_app/06cts_ubertext_start_index_drupal.html', {
        # 'TITLE': 'Calculate Chemical Speciation',
        # 'TEXT_PARAGRAPH': xx
    })

    # html = html + render_to_string('cts_app/04cts_uberoutput_end.html', {})

    html += render_to_string('cts_app/04cts_uberbatch_start.html', {
            'model': model,
            'model_attributes': header+' Batch Output'})

    # timestamp / version section
    st = datetime.datetime.strptime(Calculator().gen_jid(), 
        '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')
    html += """
    <div class="out_">
        <b>{} Batch</a><br>
    """.format(header)
    html += st
    html += " (EST)</b>"
    html += """
    </div><br><br>"""

    # Uses CSV dropdown for gentrans workflow, regular button for the rest:
    if model == 'gentrans':
        html += render_to_string('cts_app/04cts_uberoutput_end_gentrans.html')  # file download html    
    else:
        html += render_to_string('cts_app/04cts_uberoutput_end.html')  # file download html

    html = html + render_to_string('cts_app/cts_export.html', {}, request=request)

    batchOutputPageFunc = getattr(batchoutputmodule, model+'BatchOutputPage')  # function name = 'model'BatchOutputPage  (e.g. 'sipBatchOutputPage')
    html += batchOutputPageFunc(request)


    html += render_to_string('cts_app/07ubertext_end_drupal.html', {})
    # html += links_left.ordered_list(model='cts/' + model)  # fills out 05ubertext_links_left_drupal.html
    html += ordered_list(model='cts/' + model, page='batchoutput')

    #scripts and footer
    html += render_to_string('cts_app/09epa_drupal_ubertool_css.html', {})
    html += render_to_string('cts_app/09epa_drupal_cts_css.html')
    html += render_to_string('cts_app/09epa_drupal_cts_scripts.html', request=request)
    #html += render_to_string('cts_app/09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('cts_app/10epa_drupal_footer.html', {})


    response = HttpResponse()
    response.write(html)
    return response