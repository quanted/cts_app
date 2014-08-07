from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
import linksLeft

def qaqcPage(request, model='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    qaqcmodule = importlib.import_module('.'+model+'_qaqc', 'models.'+model)
    tablesmodule = importlib.import_module('.'+model+'_tables', 'models.'+model)
    from REST import rest_funcs
    header = viewmodule.header

    html = render_to_string('01cts_uberheader.html', {'title': header+' QA/QC'})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'qaqc'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04uberoutput_start.html', {
            'model':model,
            'model_attributes': header+' QAQC'})
    try:
        modelQAQC_obj = getattr(qaqcmodule, model+'_obj')      # Calling model object, e.g. 'sip_obj'
        html = html + tablesmodule.timestamp(modelQAQC_obj)
        html = html + tablesmodule.table_all_qaqc(modelQAQC_obj)
        rest_funcs.save_dic(html, modelQAQC_obj.__dict__, model, 'qaqc')
    except:
        pass
    html = html + render_to_string('export.html', {})
    html = html + render_to_string('04uberoutput_end.html', {'sub_title': ''})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})

    response = HttpResponse()
    response.write(html)
    return response