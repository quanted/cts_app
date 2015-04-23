from django.views.decorators.http import require_POST
import StringIO
from django.http import HttpResponse
from django.conf import settings
import datetime
import pytz
import json
import os

import logging


def parsePOST(request):

    pdf_t = request.POST.get('pdf_t')
    pdf_nop = request.POST.get('pdf_nop')
    pdf_p = json.loads(request.POST.get('pdf_p'))

    # Append strings and check if charts are present
    final_str = pdf_t
    final_str = final_str + """<br>"""
    if (int(pdf_nop)>0):
        for i in range(int(pdf_nop)):
            final_str = final_str + """<img id="imgChart1" src="%s" />"""%(pdf_p[i])
            # final_str = final_str + """<br>"""

    # Styling
    input_css="""
            <style>
            body {font-family: 'Open Sans', sans-serif;}
            table {
                border: 1px solid #666666;
            }
            th {text-align:center; padding:2px; font-size:11px;}
            td {padding:2px; font-size:10px; border: solid 1px #666666;}
            h2 {font-size:13px; color:#79973F;}
            h3 {font-size:12px; color:#79973F;}
            h4 {font-size:12px; color:#79973F; padding-top:30px;}
            .pdfDiv {border: 1px solid #000000;}
            div.tooltiptext {display: table;}
            </style>
            """
    input_str = input_css + final_str

    return input_str

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths for xhtml2pdf to access those resoures
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = os.path.join(settings.PROJECT_ROOT, 'static')    # Typically /home/userX/project_static/

    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    # 'media URI must start with %s or %s' % \
                    # (sUrl, mUrl))
                    'media URI must start with %s' % \
                    (sUrl))
    return path


# @require_POST
# @require_GET
def pdfReceiver(request, model=''):
    """
    PDF Generation Receiver function.
    Sends POST data as string to xhtml2pdf library for processing
    """
    from xhtml2pdf import pisa


    # Open description txt
    # text_description = open(os.path.join(os.environ['PROJECT_PATH'], 'models/'+model+'/'+model+'_text.txt'),'r')
    # description = text_description.read()
    description = ''

    # Open algorithm txt
    #text_algorithm = open(os.path.join(os.environ['PROJECT_PATH'], 'models/'+model+'/'+model+'_algorithm.txt'),'r')
    #algorithms = text_algorithm.read()

    input_str = description
    input_str += parsePOST(request)
    #input_str = input_str + algorithms         # PILlow has bug where transparent PNGs don't render correctly (black background)

    packet = StringIO.StringIO() #write to memory
    pisa.CreatePDF(input_str, dest=packet, link_callback=link_callback)

    # Create timestamp
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M')

    response = HttpResponse(packet.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.pdf'

    return response


@require_POST
def htmlReceiver(request, model=''):

    # text_description = open(os.path.join(os.environ['PROJECT_PATH'], 'models/'+model+'/'+model+'_text.txt'),'r')
    # description = text_description.read()

    description = ""

    input_str = description
    input_str += parsePOST(request)

    packet = StringIO.StringIO(input_str)  # write to memory

    # Create timestamp
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M')

    response = HttpResponse(packet.getvalue(), content_type='application/html')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.html'

    return response