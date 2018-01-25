from django.views.decorators.http import require_POST
import io
from django.http import HttpResponse
from django.template import Context
import json
from xhtml2pdf import pisa

import logging
from cts_app.cts_calcs.calculator_metabolizer import MetabolizerCalc
from cts_app.models.gentrans.gentrans_tables import buildMetaboliteTableForPDF
from django.core.cache import cache


def parsePOST(request):

    pdf_t = request.POST.get('pdf_t')
    pdf_nop = request.POST.get('pdf_nop')
    pdf_p = json.loads(request.POST.get('pdf_p'))
    if 'pdf_json' in request.POST and request.POST['pdf_json']:
        pdf_json = json.loads(request.POST.get('pdf_json'))
        # pdf_json = request.POST.get('pdf_json')
    else:
        pdf_json = None

    # Append strings and check if charts are present
    final_str = pdf_t

    if 'gentrans' in request.path:

        headings = ['genKey', 'smiles', 'iupac', 'formula', 'mass', 'exactMass', 'routes']
        calcs = ['chemaxon', 'epi', 'test', 'sparc', 'measured']
        checkedCalcsAndProps = pdf_json['checkedCalcsAndProps']
        products = pdf_json['nodes']
        props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press',
                'mol_diss', 'ion_con', 'henrys_law_con', 'kow_no_ph',
                'kow_wph', 'koc', 'water_sol_ph']

        for product in products:
            # product_image = data_walks.nodeWrapper(product['smiles'], None, 250, 100, product['genKey'], 'png', False)
            product_image = MetabolizerCalc().nodeWrapper(product['smiles'], None, 250, 100, product['genKey'], 'png', False)
            product.update({'image': product_image})

            # build object that's easy to make pchem table in template..
            if 'pchemprops' in product:

                rows = []
                for prop in props:

                    data_row = []
                    kow_no_ph_list = []
                    kow_wph_list = []
                    data_row.append(prop)

                    calc_index = 1
                    for calc in calcs:
                        # pick out data by key, make sure not already there..
                        for data_obj in product['pchemprops']:
                            if data_obj['prop'] == prop and data_obj['calc'] == calc:
                                if prop == 'kow_no_ph' and calc == 'chemaxon':
                                    # expecting same calc/prop with 3 methods..\
                                    already_there = False
                                    for item in kow_no_ph_list:
                                        if data_obj['method'] == item['method']:
                                            already_there = True
                                    if not already_there:
                                        kow_no_ph_list.append({
                                            'method': data_obj['method'],
                                            'data': round(data_obj['data'], 2)
                                        })
                                elif prop == 'kow_wph' and calc == 'chemaxon':
                                    # expecting same calc/prop with 3 methods..
                                    already_there = False
                                    for item in kow_no_ph_list:
                                        if data_obj['method'] == item['method']:
                                            already_there = True
                                    if not already_there:
                                        kow_wph_list.append({
                                            'method': data_obj['method'],
                                            'data': round(data_obj['data'], 2)
                                        })
                                    # account for kow_wph too!!!!!
                                # elif prop == 'ion_con' and calc == 'chemaxon':
                                elif prop == 'ion_con':
                                    # is there also pKb?????
                                    pka_string = ""
                                    pka_index = 1
                                    if not chem_data.get('data'):
                                        chem_data['data'] = {'pKa': []}
                                    for pka in data_obj['data']['pKa']:
                                        try:
                                            # todo: centralize rounding procedures
                                            pka_string += "pka_{}: {} \n".format(pka_index, round(pka, 2))
                                        except TypeError as te:
                                            logging.warning("pka value not a number, {}".format(te))
                                            pka_string += "pka_{}: {} \n".format(pka_index, pka)
                                        pka_index += 1
                                    data_row.append(pka_string)
                                else:
                                    data_row.append(data_obj['data'])

                        if len(data_row) <= calc_index:
                            # should mean there wasn't data for calc-prop combo:
                            data_row.append('')

                        calc_index += 1

                        if prop == 'kow_no_ph' and calc == 'chemaxon':
                            # insert chemaxon's kow values if they exist:
                            kow_string = ""
                            for kow in kow_no_ph_list:
                                kow_string += "{} ({}) \n".format(kow['data'], kow['method'])
                            # data_row.insert(1, kow_string)
                            data_row[1] = kow_string
                            # kow_values = []

                        if prop == 'kow_wph' and calc == 'chemaxon':
                            # insert chemaxon's kow values if they exist:
                            kow_string = ""
                            for kow in kow_wph_list:
                                kow_string += "{} ({}) \n".format(kow['data'], kow['method'])
                            # data_row.insert(1, kow_string)
                            data_row[1] = kow_string
                            # kow_values = []

                    rows.append(data_row)

                product['data'] = rows

        final_str += buildMetaboliteTableForPDF().render(
            Context(dict(headings=headings, checkedCalcsAndProps=checkedCalcsAndProps, products=products, props=props, calcs=calcs)))


    final_str += """<br>"""
    if (int(pdf_nop)>0):
        for i in range(int(pdf_nop)):
            final_str += """<img id="imgChart1" src="%s" />"""%(pdf_p[i])
            # final_str = final_str + """<br>"""

    # Styling
    input_css="""
            <style>
            html {
                background-color:#FFFFFF;
            }
            body {
                font-family: 'Open Sans', sans-serif;
            }
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

            #pchemprop_table table {
                width: 100%;
                overflow: auto;
                border: 1px solid #666666;
                display: table;
                border-collapse: collapse;
            }
            #pchemprop_table tr {
                border: 1px solid #666666;
                display: table-row;
            }
            #pchemprop_table td, #pchemprop_table th {
                word-break: break-all;
                border: 1px solid #666666;
                display: table-cell;
            }

            th {text-align:center; padding:2px; font-size:11px;}
            td {padding:2px; font-size:10px;}
            h2 {font-size:13px; color:#79973F;}
            h3 {font-size:12px; color:#79973F; margin-top: 8px;}
            h4 {font-size:12px; color:#79973F; padding-top:30px;}
            .pdfDiv {border: 1px solid #000000;}
            div.tooltiptext {display: table; border: 1px solid #333333; margin: 8px; padding: 4px}

            div {
                background-color: #FFFFFF;
            }
            img {
                background-color: #FFFFFF;
            }

            </style>
            """
    input_str = input_css + final_str

    return input_str


@require_POST
def pdfReceiver(request, model=''):
    """
    PDF Generation Receiver function.
    Sends POST data as string for processing
    """

    input_str = ''
    input_str += parsePOST(request)
    packet = io.StringIO()  # write to memory

    try:
        pisa.CreatePDF(input_str, dest=packet)
    except ValueError as error:
        # triggered from the elusive invalid color value issue:
        logging.warning("elusive invalid color value, defaulting html background-color to FFFFFF")
        pisa.CreatePDF(input_str, dest=packet, default_css="body{background-color:#FFFFFF;}")


    jid = MetabolizerCalc().gen_jid()  # create timestamp
    response = HttpResponse(packet.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.pdf'
    packet.close()  # todo: figure out why this doesn't solve the 'caching problem'
    return response


@require_POST
def htmlReceiver(request, model=''):
    """
    Save output as HTML
    """
    input_str = ''
    input_str += parsePOST(request)
    packet = io.StringIO(input_str)  # write to memory
    jid = MetabolizerCalc().gen_jid()  # create timestamp
    response = HttpResponse(packet.getvalue(), content_type='application/html')
    response['Content-Disposition'] = 'attachment; filename=' + model + '_' + jid + '.html'
    # packet.truncate(0)  # clear from memory?
    packet.close()
    return response


@require_POST
def csvReceiver(request, model=''):
    """
    Save output as CSV
    """
    from .downloads_cts import CSV
    from django.conf import settings

    settings.DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB => 10485760 bytes (IEC units)
    logging.warning("DJANGO MAX UPLOAD MEM: {}".format(settings.DATA_UPLOAD_MAX_MEMORY_SIZE))

    try:
        request_data = request.POST.get('run_data')
        run_data = json.loads(request_data)
    except Exception as error:
        logging.warning("CSV ERROR: {}".format(error))
        raise error

    csv_obj = CSV(model)
    return csv_obj.parseToCSV(run_data)