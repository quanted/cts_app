from django.template.loader import render_to_string
from django.http import HttpResponse
import importlib
import linksLeft
import os

def referencesPage(request, model='none', header='none'):
    viewmodule = importlib.import_module('.views', 'models.'+model)
    header = viewmodule.header

    text_file1 = open(os.path.join(os.environ['PROJECT_PATH'], 'models/'+model+'/'+model+'_references.txt'),'r')
    x = text_file1.read()
    html = render_to_string('01cts_uberheader.html', {'title': header+' References'})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'references'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04uberreferences_start.html', {
            'model_attributes': header+' References', 
            'text_paragraph':x})
    html = html + render_to_string('04ubertext_end.html', {})
    html = html + render_to_string('05cts_ubertext_links_right.html', {})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
    
    response = HttpResponse()
    response.write(html)
    return response