import importlib
import os

from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from .links_left import ordered_list
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def inputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    inputmodule = importlib.import_module('.'+model+'_input', 'cts_app.models.'+model)
    header = viewmodule.header

    # 2017 drupal template
    html = render_to_string('01cts_epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })

    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})
    html += render_to_string('06cts_ubertext_start_index_drupal.html', {})

    inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    html += inputPageFunc(request, model, header)

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list(model='cts/' + model, page='input')

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html', request=request)
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response