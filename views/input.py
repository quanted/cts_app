import importlib
import os

from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
#from .linksLeft import linksLeft
from .links_left import ordered_list
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def inputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    inputmodule = importlib.import_module('.'+model+'_input', 'cts_app.models.'+model)
    header = viewmodule.header


    #drupal template for header with bluestripe
    #html = render_to_string('01epa_drupal_header.html', {})
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    #html = render_to_string('01uberheader_main_drupal.html', {
    #    'SITE_SKIN': os.environ['SITE_SKIN'],
    #    'TITLE': u"\u00FCbertool"
    #})
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})

    #main body of text
    #html += render_to_string('04uber_drupal_frog_intro.html', {})
    #http://jsfiddle.net/9zGQ8/

    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        # 'TITLE': 'Calculate Chemical Speciation',
        # 'TEXT_PARAGRAPH': xx
    })


    inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    html += inputPageFunc(request, model, header)


    html += render_to_string('07ubertext_end_drupal.html', {})
    # html += links_left.ordered_list(model='cts/' + model)  # fills out 05ubertext_links_left_drupal.html
    html += ordered_list(model='cts/' + model, page='input')

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')

    print("request object: {}".format(dir(request)))

    # sending request to template with scripts_jchem added (will this work if template imports js and isn't in template itself?)
    html += render_to_string('09epa_drupal_cts_scripts.html', request=request)
    #html += render_to_string('09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})


    # html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
    # html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
    # html = html + linksLeft.linksLeft()

    # inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    # html = html + inputPageFunc(request, model, header)

    # html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
    
    response = HttpResponse()
    response.write(html)
    return response