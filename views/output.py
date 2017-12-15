import importlib
import logging
import os

from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .linksLeft import linksLeft
from .links_left import ordered_list
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def outputPageView(request, model='none', header=''):

    outputmodule = importlib.import_module('.'+model+'_output', 'cts_app.models.'+model)
    tablesmodule = importlib.import_module('.'+model+'_tables', 'cts_app.models.'+model)

    outputPageFunc = getattr(outputmodule, model+'OutputPage') # function name = 'model'OutputPage  (e.g. 'sipOutputPage')
    model_obj = outputPageFunc(request)

    if type(model_obj) is tuple:
        modelOutputHTML = model_obj[0]
        model_obj = model_obj[1]
    else:
        # logging.info(model_obj.__dict__)
        modelOutputHTML = tablesmodule.timestamp(model_obj)

        tables_output = tablesmodule.table_all(model_obj)
        
        if type(tables_output) is tuple:
            modelOutputHTML = modelOutputHTML + tables_output[0]
        elif type(tables_output) is str or type(tables_output) is unicode:
            modelOutputHTML = modelOutputHTML + tables_output
        else:
            modelOutputHTML = "table_all() Returned Wrong Type"

     #drupal template for header with bluestripe
    #html = render_to_string('01epa_drupal_header.html', {})
    html = render_to_string('01epa_drupal_header.html', {
        'SITE_SKIN': os.environ['SITE_SKIN'],
        'title': "CTS"
    })
    html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
    html += render_to_string('03epa_drupal_section_title_cts.html', {})
    html += render_to_string('06cts_ubertext_start_index_drupal.html', {
        # 'TITLE': 'Calculate Chemical Speciation',
        # 'TEXT_PARAGRAPH': xx
    })

    html += render_to_string('04cts_uberoutput_end.html', {'model':model})  # file download html

    html += render_to_string('04cts_uberoutput_start.html', {
            'model_attributes': header+' Output'})


    # html += '<div>'
    # html += render_to_string('04cts_uberoutput_end.html', {'model':model})  # file download html


    html += modelOutputHTML

    html = html + render_to_string('cts_export.html', {}, request=request)
    # html += render_to_string('04cts_uberoutput_end.html', {'model':model})

    html += render_to_string('07ubertext_end_drupal.html', {})
    html += ordered_list(model='cts/' + model, page="output")  # fills out 05ubertext_links_left_drupal.html

    #scripts and footer
    html += render_to_string('09epa_drupal_ubertool_css.html', {})
    html += render_to_string('09epa_drupal_cts_css.html')
    html += render_to_string('09epa_drupal_cts_scripts.html')
    #html += render_to_string('09epa_drupal_ubertool_scripts.html', {})
    html += render_to_string('10epa_drupal_footer.html', {})

    # # Render output page view
    # html = render_to_string('01cts_uberheader.html', {'title': header+' Output'})
    # html += render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'output'})
    # html += linksLeft.linksLeft()
    # html += render_to_string('cts_export.html', {})
    # html += render_to_string('04cts_uberoutput_start.html', {
    #         'model_attributes': header+' Output'})

    # html += modelOutputHTML
    # # html = html + render_to_string('export.html', {})
    # html += render_to_string('04cts_uberoutput_end.html', {'model':model})
    # html += render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)
    return response

@require_POST
def outputPage(request, model='none', header=''):

    viewmodule = importlib.import_module('.views', 'cts_app.models.'+model)

    header = viewmodule.header

    logging.warning("HEADER: {}".format(header))

    parametersmodule = importlib.import_module('.'+model+'_parameters', 'cts_app.models.'+model)

    logging.warning("HERE WE ARE IN THE OUTPUT PAGE. GREAT.")
    logging.warning("MODEL: {}".format(model))
    logging.warning("REQUEST: {}".format(request.POST))


    try:
        # Class name must be ModelInp, e.g. SipInp or TerrplantInp
        inputForm = getattr(parametersmodule, model.title() + 'Inp')
        
        form = inputForm(request.POST) # bind user inputs to form object

        # logging.warning("FORM: {}".format(form))

        # Form validation testing
        if form.is_valid():

            logging.warning("IS VALID")

            return outputPageView(request, model, header)

        else:

            logging.warning("IS NOT VALID")
            logging.warning("ERRORS: {}".format(form.errors))

            inputmodule = importlib.import_module('.'+model+'_input', 'cts_app.models.'+model)

            # Render input page view with POSTed values and show errors
            html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
            html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
            html = html + linksLeft()

            inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
            html = html + inputPageFunc(request, model, header, formData=request.POST)  # formData contains the already POSTed form data

            html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
            
            response = HttpResponse()
            response.write(html)
            return response

        # end form validation testing

    except:
        
        logging.warning("E X C E P T")

        return outputPageView(request, model, header)
