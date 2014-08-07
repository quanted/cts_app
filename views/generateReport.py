from django.views.decorators.http import require_POST
import StringIO
from django.http import HttpResponse
import datetime
import pytz
import json

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
            final_str = final_str + """<br>"""

    # Styling
    input_css="""
            <style>
            table {margin-bottom:16px; border: 1px solid #666666;}
            th {text-align:center; padding:2px; font-size:12px;}
            td {text-align:center; padding:2px; font-size:11px;}
            h2 {font-size:13px; color:#79973F}
            h3 {font-size:12px; color:#79973F}
            h4 {font-size:12px; color:#79973F}
            </style>
            """
    input_str = input_css + final_str

    return input_str


@require_POST
def pdfReceiver(request, model=''):

    from xhtml2pdf import pisa

    input_str = parsePOST(request)

    packet = StringIO.StringIO() #write to memory
    pisa.CreatePDF(input_str, dest=packet)

    # Create timestamp
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M')

    response = HttpResponse(packet.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.pdf'
    
    return response


@require_POST
def htmlReceiver(request, model=''):

    input_str = parsePOST(request)

    packet = StringIO.StringIO(input_str) #write to memory

    # Create timestamp
    ts = datetime.datetime.now(pytz.UTC)
    localDatetime = ts.astimezone(pytz.timezone('US/Eastern'))
    jid = localDatetime.strftime('%Y%m%d%H%M')

    response = HttpResponse(packet.getvalue(), content_type='application/html')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.html'
    
    return response