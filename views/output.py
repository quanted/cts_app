from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import importlib
import linksLeft
import logging


def outputPageView(request, model='none', header=''):

    outputmodule = importlib.import_module('.'+model+'_output', 'models.'+model)
    tablesmodule = importlib.import_module('.'+model+'_tables', 'models.'+model)
    # from REST import rest_funcs

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

    # Render output page view
    html = render_to_string('01cts_uberheader.html', {'title': header+' Output'})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'output'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04uberoutput_start.html', {
            'model_attributes': header+' Output'})
    html = html + modelOutputHTML
    html = html + render_to_string('export.html', {})
    html = html + render_to_string('04uberoutput_end.html', {'model':model})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
    
    # Handle Trex, which is not objectified yet
    # if model != 'trex':
    #     rest_funcs.save_dic(html, model_obj.__dict__, model, "single")

    response = HttpResponse()
    response.write(html)
    return response

@require_POST
def outputPage(request, model='none', header=''):

    viewmodule = importlib.import_module('.views', 'models.'+model)

    header = viewmodule.header

    parametersmodule = importlib.import_module('.'+model+'_parameters', 'models.'+model)

    try:
        # Class name must be ModelInp, e.g. SipInp or TerrplantInp
        inputForm = getattr(parametersmodule, model.title() + 'Inp')
        
        form = inputForm(request.POST) # bind user inputs to form object

        # Form validation testing
        if form.is_valid():
            return outputPageView(request, model, header)

        else:
            logging.info(form.errors)
            inputmodule = importlib.import_module('.'+model+'_input', 'models.'+model)

            # Render input page view with POSTed values and show errors
            html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
            html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
            html = html + linksLeft.linksLeft()

            inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
            html = html + inputPageFunc(request, model, header, formData=request.POST)  # formData contains the already POSTed form data

            html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
            
            response = HttpResponse()
            response.write(html)
            return response

        # end form validation testing

    except:
        
        logging.info("E X C E P T")

        return outputPageView(request, model, header)