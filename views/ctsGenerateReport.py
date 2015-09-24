from django.views.decorators.http import require_POST
import StringIO
from django.http import HttpResponse
from django.conf import settings
from django.template import Context
import datetime
import pytz
import json
import os
import pdfkit

import logging
from models.gentrans import data_walks
from models.gentrans.gentrans_tables import buildMetaboliteTableForPDF
from chemaxon_cts.jchem_rest import gen_jid
import csv


def parsePOST(request):

    pdf_t = request.POST.get('pdf_t')
    pdf_nop = request.POST.get('pdf_nop')
    pdf_p = json.loads(request.POST.get('pdf_p'))
    if 'pdf_json' in request.POST and request.POST['pdf_json']:
        pdf_json = json.loads(request.POST.get('pdf_json'))
        logging.info(">>> JSON: {}".format(pdf_json))
        # pdf_json = request.POST.get('pdf_json')
    else:
        pdf_json = None

    # Append strings and check if charts are present
    final_str = pdf_t

    if 'gentrans' in request.path:
        # TODO: class this, e.g., Metabolizer (jchem_rest)
        # headings = ['genKey', 'smiles', 'water_sol', 'ion_con', 'kow_no_ph', 'kow_wph', 'image']
        headings = ['genKey', 'smiles', 'melting_point', 'boiling_point', 'water_sol', 'vapor_press',
                    'mol_diss', 'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'koc', 'image']
        metaboliteList = data_walks.buildTableValues(pdf_json, headings, 3)  # List of dicts, which are node data
        final_str += buildMetaboliteTableForPDF().render(Context(dict(headings=headings, metaboliteList=metaboliteList)))

    final_str += """<br>"""
    if (int(pdf_nop)>0):
        for i in range(int(pdf_nop)):
            final_str += """<img id="imgChart1" src="%s" />"""%(pdf_p[i])
            # final_str = final_str + """<br>"""

    # Styling
    input_css="""
            <style>

            body {font-family: 'Open Sans', sans-serif;}
            table, td, th {
                border: 1px solid #666666;
            }
            #gentrans_table td {
                /*word-wrap: normal;*/
                max-width: 100px;
                word-break: break-all;
            }
            table#inputsTable td {
                max-width: 600px;
                word-break: break-all;
            }
            table {border-collapse: collapse;}
            th {text-align:center; padding:2px; font-size:11px;}
            td {padding:2px; font-size:10px;}
            h2 {font-size:13px; color:#79973F;}
            h3 {font-size:12px; color:#79973F; margin-top: 8px;}
            h4 {font-size:12px; color:#79973F; padding-top:30px;}
            .pdfDiv {border: 1px solid #000000;}
            div.tooltiptext {display: table; border: 1px solid #333333; margin: 8px; padding: 4px}

            </style>
            """
    input_str = input_css + final_str

    return input_str


@require_POST
def pdfReceiver(request, model=''):
    """
    PDF Generation Receiver function.
    Sends POST data as string to pdfkit library for processing
    """
    input_str = ''
    input_str += parsePOST(request)
    packet = StringIO.StringIO(input_str) #write to memory
    config = pdfkit.configuration(wkhtmltopdf=os.environ['wkhtmltopdf'])
    # landscape only for metabolites output:
    if 'pdf_json' in request.POST and request.POST['pdf_json']:
        options = {'orientation': 'Landscape'}
    else:
        options = {'orientation': 'Portrait'}
    pdf = pdfkit.from_string(input_str, False, configuration=config, options=options)
    jid = gen_jid() # create timestamp
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.pdf'
    # packet.truncate(0)  # clear from memory?
    packet.close()  # todo: figure out why this doesn't solve the 'caching problem'
    return response


@require_POST
def htmlReceiver(request, model=''):
    """
    Save output as HTML
    """
    input_str = ''
    input_str += parsePOST(request)
    packet = StringIO.StringIO(input_str)  # write to memory
    jid = gen_jid() # create timestamp
    response = HttpResponse(packet.getvalue(), content_type='application/html')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.html'
    # packet.truncate(0)  # clear from memory?
    packet.close()
    return response

@require_POST
def csvReceiver(request, model=''):
    """
    Save output as HTML
    """

    logging.info("INSIDE CSV RECEIVER")

    json_data = request.POST.get('pdf_json')
    json_dict = json.loads(json_data)
    headers = json_dict['headers']
    data = json_dict['data']

    logging.info(json_data)
    logging.info(headers)
    logging.info(data)

    # input_str = ''
    # input_str += parsePOST(request)
    # packet = StringIO.StringIO(input_str)  # write to memory
    jid = gen_jid() # create timestamp
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.csv'

    writer = csv.writer(response)
    writer.writerow(headers)

    for prop, prop_vals in data.items():
        # logging.info("prop: {}".format(prop))
        # logging.info("vals: {}".format(prop_vals))
        row = prop_vals
        row.insert(0, prop) # prepend row with prop label
        logging.info("row: {}".format(row))
        writer.writerow(row)


    # writer.writerow(['First row', 'a', 'b', 'c'])
    # writer.writerow(['Second row', 'a', 'b', 'c'])
    # writer.writerow(['', 'calc1', 'calc2', 'calc3']) <-- headers
    # writer.writerow(['', '', '', ''])
    # writer.writerow(['prop_name', 'val1', 'val2', 'val3']) <-- arrays of data by prop


    # packet.truncate(0)  # clear from memory?
    # packet.close()
    return response


# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths for xhtml2pdf to access those resoures
#     """
#     # use short variable names
#     sUrl = settings.STATIC_URL      # Typically /static/
#     sRoot = os.path.join(settings.PROJECT_ROOT, 'static')    # Typically /home/userX/project_static/

#     if uri.startswith(sUrl):
#         path = os.path.join(sRoot, uri.replace(sUrl, ""))

#     # make sure that file exists
#     if not os.path.isfile(path):
#             raise Exception(
#                     # 'media URI must start with %s or %s' % \
#                     # (sUrl, mUrl))
#                     'media URI must start with %s' % \
#                     (sUrl))
#     return path