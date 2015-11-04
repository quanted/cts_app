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


class CSV(object):
    def __init__(self, model):
        self.models = ['chemspec', 'pchemprop', 'gentrans']
        self.calcs = ['chemaxon', 'epi', 'test', 'sparc']
        self.props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss', 
                        'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'kow_ph', 'koc']
        if model and (model in self.models):
            self.model = model # model name
        else:
            raise KeyError("Model - {} - not accepted..".format(model))
        self.title = '' # workflow title
        self.time = '' # time of run
        self.csv_rows = [], # ordered list of list (header, row1, ...)
        self.parent_info = ['smiles', 'name', 'mass', 'formula'] # original user sructure
        self.header_row = [] # headers in order (per molecule)
        self.data_row = [] # data in order w/ headers
        self.run_json = '' # json str from [model]_model.py
        self.run_data = {} # run_json as an object

    def parseToCSV(self, run_data):
        jid = gen_jid() # create timestamp
        time_str = datetime.datetime.strptime(jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + self.model + '_' + jid + '.csv'

        writer = csv.writer(response) # bind writer to http response

        # build title section of csv..
        writer.writerow([run_data['title']])
        writer.writerow([run_data['time']])
        writer.writerow([""])

        # header_row = []
        # self.csv_rows.append(header_row) # add header list to csv_rows list..
        rows = [[], []] # initialized with header and first row..

        # write parent info first and in order..
        for prop in self.parent_info:
            for key, val in run_data.items():
                if key == prop:
                    rows[0].append(key)
                    rows[1].append(val)

        if self.model == 'chemspec':
            for key, val in run_data.items():
                if key not in self.parent_info:
                    if key == 'isoelectricPoint':
                        rows[0].append(key)
                        rows[1].append(val)
                    elif key == 'pka' or key == 'pkb':
                        i = 0 # pka counter
                        for item in val:
                            rows[0].append(key + str(i))
                            rows[1].append(item)
                            i+=1
                    elif key == 'pka-parent' or key == 'majorMicrospecies':
                        rows[0].append(key + '-smiles')
                        rows[1].append(val['smiles'])
                    elif key == 'pka-micospecies':
                        for ms in val.items():
                            # each ms is a jchem_structure object
                            rows[0].append(key + '-smiles')
                            rows[1].append(val['smiles'])
                    elif key == 'stereoisomers' or key == 'tautomers':
                        i = 0
                        for item in val:
                            rows[0].append(item['key'] + str(i))
                            rows[1].append(item['smiles'])
                            i+=1

        elif self.model == 'pchemprop':
            for prop in self.props:
                for calc, calc_props in run_data.items():
                    if prop in calc_props:
                        if prop == "ion_con":
                            for pka_key, pka_val in calc_props[prop].items():
                                rows[0].append("{} ({})".format(pka_key, calc))
                                rows[1].append(pka_val)
                        else:   
                            rows[0].append("{} ({})".format(prop, calc))
                            rows[1].append(calc_props[prop])


        elif self.model == 'gentrans':
            # TODO: class this, e.g., Metabolizer (jchem_rest)

            # fileout = open("C:\\Users\\nickpope\\Desktop\\out.txt", "w")
            # fileout.write(json.dumps(run_data['pdf_json']))
            # fileout.close()

            ###################################################################
            filein = open("C:\\Users\\nickpope\\Desktop\\out2.txt", "r")
            exjson = json.loads(filein.read())
            filein.close()
            ###################################################################

            logging.info(">>> FILE CONTENT: {} <<<".format(exjson))

            # metabolites_data = run_data['pdf_json']
            metabolites_data = exjson # hard coded metabolites json for now...

            if not metabolites_data:
                return HttpResponse("error building csv for metabolites..")

            m = 1 # metabolite indexer
            rows[0].insert(0, "gen") # insert generation header first
            # metabolite per row...
            for metabolite in metabolites_data:

                # add another row (list) to rows, prevent out of range errors (temp fix..)
                if m >= len(rows):
                    rows.append([])

                # # add genkey..
                # rows[0].insert(0, "gen")
                rows[m].insert(0, metabolite['genKey'])

                # # add smiles..
                # rows[0].append("smiles")
                if m > 1:
                    rows[m].append(metabolite['smiles'])
                    # TODO: get name, mass, formula for each metabolite to remove below craziness..
                    rows[m].extend(('', '', '')) # skipping name, mass, formula columns for metabolites

                # below prop/calc loops for ordering row by prop..
                for prop in self.props:
                    for calc in self.calcs:
                        if 'pchemprops' in metabolite:
                            for data_obj in metabolite['pchemprops']:

                                # now for the metabolite pchem data..
                                met_prop = data_obj['prop']
                                met_calc = data_obj['calc']
                                met_data = data_obj['data']

                                if met_prop == prop and met_calc == calc:
                                    if met_prop != 'ion_con':
                                        rows[0].append("{} ({})".format(met_prop, met_calc))
                                        rows[m].append(met_data)
                                    else:
                                        for key, val in data_obj['data'].items():
                                            i = 0
                                            for pka in val:
                                                rows[0].append("{}{} ({})".format(key, i, calc))
                                                rows[m].append(pka)
                                                i+=1
                m+=1 # increment metabolite indexer

        # loop csv rows instead of hard-coded 'row_1' shenanigans..
        writer.writerow(rows[0]) # append header row to csv..
        for row in rows[1:]:
            writer.writerow(row)

        return response


@require_POST
def csvReceiver(request, model=''):
    """
    Save output as CSV
    """
    cache_key = "{}_json".format(model) # model-specific cache 

    try:
        run_json = cache.get(cache_key) # todo: add error handling
        cache.delete(cache_key)
        run_data = json.loads(run_json)
    except TypeError as te:
        logging.info("CSV ERROR: {}".format(te))
        return None

    if model == 'pchemprop':
        try:
            json_data = request.POST.get('pdf_json') # checkCalcsAndProps dict
            run_data.update(json.loads(json_data))
        except Exception as err:
            raise err

    elif model == 'gentrans':

        logging.info(cache.get('pchemprop_json'))

        try:
            json_data = request.POST.get('pdf_json') # checkCalcsAndProps dict
            run_data.update({'pdf_json': json.loads(json_data)})
        except Exception as err:
            logging.warning("!!! csv error: {} !!!".format(err))
            raise err

    csv_obj = CSV(model)
    return csv_obj.parseToCSV(run_data)