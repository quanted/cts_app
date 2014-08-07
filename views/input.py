from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
import importlib
import linksLeft

def inputPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    inputmodule = importlib.import_module('.'+model+'_input', 'models.'+model)
    header = viewmodule.header

    # import logging

    # if formData != None:
    #     logging.info("===================== N O N E ==========================")
    #     html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
    #     html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
    #     html = html + linksLeft.linksLeft()

    #     inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    #     html = html + inputPageFunc(request, model, header, formData)

    #     html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
        
    #     response = HttpResponse()
    #     response.write(html)
    #     return response

    # VALIDATE FORM HERE IF FORM IS POSTED TO THIS VIEW
    # if request.method == "POST":
    #     parametersmodule = importlib.import_module('.'+model+'_parameters', 'models.'+model)
    #     inputForm = getattr(parametersmodule, model.upper() + 'Inp')
        
    #     logging.info(inputForm)
    #     form = inputForm(request.POST)
        
    #     logging.info(form)
        
    #     if form.is_valid():
    #         outputmodule = importlib.import_module('.'+model+'_output', 'models.'+model)
    #         return outputmodule(request)
    #     else:
    #         html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
    #         html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
    #         html = html + linksLeft.linksLeft()

    #         inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    #         html = html + inputPageFunc(request, model, header, formData=request.POST)

    #         html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
            
    #         response = HttpResponse()
    #         response.write(html)
    #         return response
    
    # else:
    html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
    html = html + render_to_string('cts-jquery.html', {})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
    html = html + linksLeft.linksLeft()

    inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
    html = html + inputPageFunc(request, model, header)

    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
    
    response = HttpResponse()
    response.write(html)
    return response