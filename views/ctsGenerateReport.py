from django.views.decorators.http import require_POST
import io
from django.http import HttpResponse
from django.template import Context
import json
from xhtml2pdf import pisa
import logging
from cts_app.cts_calcs.calculator_metabolizer import MetabolizerCalc
from cts_app.models.gentrans.gentrans_tables import buildMetaboliteTableForPDF
from .downloads_cts import CSV, roundData
from django.core.cache import cache
from django.conf import settings



def parsePOST(request):

	pdf_t = request.POST.get('pdf_t')
	pdf_nop = request.POST.get('pdf_nop')
	pdf_p = json.loads(request.POST.get('pdf_p'))
	if 'pdf_json' in request.POST and request.POST['pdf_json']:
		pdf_json = json.loads(request.POST.get('pdf_json'))
	else:
		pdf_json = None

	# Append strings and check if charts are present
	final_str = pdf_t

	if 'gentrans' in request.path:
		final_str += handle_gentrans_request(pdf_json)  # add metabolites to PDF/HTML file

	final_str += "<br>"
	if (int(pdf_nop)>0):
		for i in range(int(pdf_nop)):
			final_str += """<img id="imgChart1" src="%s" />"""%(pdf_p[i])


	# PDF/HTML File Styling:
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
				max-width: 100px;
				word-break: break-all;
			}
			#pchemprop_table table {
				width: 100%;
				overflow: auto;
				display: table;
			}
			#pchemprop_table tr {
				display: table-row;
			}
			#pchemprop_table td, #pchemprop_table th {
				word-break: break-all;
				display: table-cell;
			}

			th {text-align:center; padding:2px; font-size:11px;}
			td {padding:2px; font-size:10px; margin:2px;}
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
	# packet = io.StringIO()  # write to memory
	packet = io.BytesIO()

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
	from django.conf import settings

	settings.DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB => 10485760 bytes (IEC units)

	try:
		request_data = request.POST.get('run_data')
		run_data = json.loads(request_data)
	except Exception as error:
		logging.warning("CSV ERROR: {}".format(error))
		raise error

	csv_obj = CSV(model)
	return csv_obj.parseToCSV(run_data)


def textReceiver(request, model=''):
	"""
	Download text file.
	"""
	static_path = "{}/static_qed/cts/docs/sample_batch.txt".format(settings.PROJECT_ROOT.replace('\\', '/'))
	filein = open(static_path, 'rb')
	sample_batch_text = filein.read().decode('utf-16')
	filein.close()
	response = HttpResponse(sample_batch_text, content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=sample_batch.txt'
	return response


def handle_gentrans_request(pdf_json):

	headings = ['genKey', 'routes', 'smiles', 'iupac', 'formula', 'mass', 'exactMass', 'accumulation', 'production', 'globalAccumulation', 'likelihood']
	calcs = ['chemaxon', 'epi', 'test', 'sparc', 'measured']
	checkedCalcsAndProps = pdf_json['checkedCalcsAndProps']
	products = pdf_json['nodes']
	props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press',
			'mol_diss', 'mol_diss_air', 'ion_con', 'henrys_law_con', 'kow_no_ph',
			'kow_wph', 'koc', 'water_sol_ph', 'log_bcf', 'log_baf']

	for product in products:
		# product_image = data_walks.nodeWrapper(product['smiles'], None, 250, 100, product['genKey'], 'png', False)
		product_image = MetabolizerCalc().nodeWrapper(product['smiles'], None, 250, 100, product['genKey'], 'png', True)
		product.update({'image': product_image})

		# build object that's easy to make pchem table in template..
		if not 'pchemprops' in product:
			continue

		rows = []
		method_map = {}

		for prop in props:

			data_row = []
			data_row.append(prop)

			calc_index = 1
			for calc in calcs:

				method_map[calc] = {}
				method_map[calc][prop] = []

				# pick out data by key, make sure not already there..
				for data_obj in product['pchemprops']:

					if data_obj['prop'] != prop or data_obj['calc'] != calc:
						continue

					if data_obj.get('method'):
						# if the calc's property has methods, append them as one string
						# for the table cell:

						already_there = False
						for item in method_map[calc][prop]:
							if data_obj['method'] == item['method']:
								already_there = True

						if not already_there:

							method_obj = {}
							method_obj['method'] = data_obj['method']

							method_obj['data'] = roundData(prop, data_obj['data'])

							# try:
							# 	# tries rounding value if it's numeric:
							# 	method_obj['data'] = round(data_obj['data'], 3)
							# except TypeError:
							# 	# if not numeric, stores as-is:
							# 	method_obj['data'] = data_obj['data']

							method_map[calc][prop].append(method_obj)

					elif prop == 'ion_con':
						pka_string = ""
						pka_index = 1
						if not data_obj.get('data'):
							data_obj['data'] = {'pKa': []}
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
						# data_row.append(data_obj['data'])
						data_row.append(roundData(prop, data_obj['data']))

				if len(data_row) <= calc_index:
					# should mean there wasn't data for calc-prop combo:
					data_row.append('')

				if len(method_map[calc][prop]) > 0:
					# if calc-prop data has methods, build them as a string
					# for a single table cell:
					table_cell_string = ""
					for item in method_map[calc][prop]:
						table_cell_string += "{} ({})\n".format(roundData(prop, item['data']), item['method'])
					data_row[calc_index] = table_cell_string

				calc_index += 1

			rows.append(data_row)

		product['data'] = rows

	# Adds geomean to product's 'data' lists:
	products = add_geomean_to_products(products)

	return buildMetaboliteTableForPDF().render(
		Context(dict(headings=headings, checkedCalcsAndProps=checkedCalcsAndProps, products=products, props=props, calcs=calcs)))




def add_geomean_to_products(products):
	"""
	Adds geomean data to products data for building
	a PDF for the gentrans workflow.
	"""
	for product in products:
		if not 'geomeanDict' in product:
			continue
		for prop_name, geomean_val in product['geomeanDict'].items():
			if not geomean_val:
				continue
			# add geomean val to property in product's data
			product = add_geomean_to_product_data(product, prop_name, geomean_val)
		product = fill_empty_geomean_vals(product)
	return products



def add_geomean_to_product_data(product, prop_name, geomean_val):
	"""
	Adds geomean data to the product's data by property.
	"""
	for prop_data_list in product['data']:
		if prop_data_list[0] == prop_name:
			# prop_data_list.append(geomean_val)
			prop_data_list.insert(len(prop_data_list)-1, roundData(prop_name, geomean_val))  # inserts geomean before Measured column
	return product



def fill_empty_geomean_vals(product):
	"""
	Fills any empty geomean values for a product.
	"""
	headers = ['chemaxon', 'epi', 'test', 'sparc', 'geomean', 'measured']
	for prop_data_list in product['data']:
		if len(prop_data_list) < len(headers):
			prop_data_list.append('')
	return product
