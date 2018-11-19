import importlib
import logging
import os

from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .links_left import ordered_list
from .generate_timestamp import get_timestamp
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def outputPageView(request, model='none', header=''):

    outputmodule = importlib.import_module('.'+model+'_output', 'cts_app.models.'+model)
    tablesmodule = importlib.import_module('.'+model+'_tables', 'cts_app.models.'+model)
    # titlemodule = importlib.import_module('.views', 'cts_app.models.'+model)

    outputPageFunc = getattr(outputmodule, model+'OutputPage') # function name = 'model'OutputPage  (e.g. 'sipOutputPage')
    model_obj = outputPageFunc(request)

    if type(model_obj) is tuple:
        modelOutputHTML = model_obj[0]
        model_obj = model_obj[1]
    else:
        modelOutputHTML = get_timestamp(model_obj)
        tables_output = tablesmodule.table_all(model_obj)
        
        if type(tables_output) is tuple:
            modelOutputHTML = modelOutputHTML + tables_output[0]
        elif type(tables_output) is str:
            modelOutputHTML = modelOutputHTML + tables_output
        else:
            modelOutputHTML = "table_all() Returned Wrong Type"

    # drupal template for header with bluestripe
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})
    html += render_to_string('06cts_ubertext_start_index_drupal.html', {})

    html += render_to_string('04cts_uberoutput_end.html', {'model':model})  # file download html

    html += render_to_string('04cts_uberoutput_start.html', {
            'model_attributes': header+' Output'})

    html += modelOutputHTML

    html = html + render_to_string('cts_export.html', {}, request=request)

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list(model='cts/' + model, page="output")  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    html += render_to_string('10epa_drupal_footer.html', {})

    response = HttpResponse()
    response.write(html)
    return response

@require_POST
def outputPage(request, model='none', header=''):

    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)
    header = viewmodule.header

    parametersmodule = importlib.import_module('.'+model+'_parameters', 'cts_app.models.'+model)

    try:
        # Class name must be ModelInp, e.g. SipInp or TerrplantInp
        inputForm = getattr(parametersmodule, model.title() + 'Inp')
        form = inputForm(request.POST) # bind user inputs to form object

        # Form validation testing
        if not form.is_valid():
            return generate_error_page(model)

        return outputPageView(request, model, header)

    except Exception as e:
        return generate_error_page(model)



def generate_error_page(model, title=None, error_msg=None):
    """
    Generates error page to display to user if something went wrong.
    """

    if not title or not error_msg:
        title = 'Error processing model'
        error_msg = """
        <p>A error occurred while processing the submitting model. Please check the model inputs and try again.</p>

        <form action="/cts/{}/input" method="get">
            <input type="submit" value="Go back to input page" />
        </form>
        """.format(model)

    html = render_to_string('01epa_drupal_header.html', {
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

    response = HttpResponse()
    response.write(html)
    return response