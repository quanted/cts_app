__author__ = 'np'

"""
Moving PDF, HTML, and CSV stuff from ctsGenerateReport in the views folder to
this file in the REST directory. For now though, I'm just going to add the 
CSV class here. ctsGenerateReport will still be an entry point that will make
calls to this file.
"""
import csv
import json
import datetime
import logging
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from ..cts_calcs.calculator_chemaxon import JchemCalc
from ..cts_calcs.calculator_epi import EpiCalc
from ..cts_calcs.calculator_test import TestWSCalc
from ..cts_calcs.calculator_sparc import SparcCalc


class CSV(object):
	def __init__(self, model):
		self.models = ['chemspec', 'pchemprop', 'gentrans']
		self.calcs = ['chemaxon', 'epi', 'test', 'sparc']
		self.props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss', 'mol_diss_air',
					  'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'kow_ph', 'koc', 'water_sol_ph', 'log_bcf', 'log_baf']
		self.speciation_props = ['isoelectricPoint', 'pka', 'pkb', 'majorMicrospecies', 'pka_microspecies']
		if model and (model in self.models):
			self.model = model  # model name
		else:
			raise KeyError("Model - {} - not accepted..".format(model))
		self.molecular_info = ['smiles', 'iupac', 'formula', 'mass', 'exactMass']  # original user sructure

		self.new_phkow_key = "d_ow"  # key to use for csv for kow_wph


	def insert_rows(self, rows, header_index, chem_data, spec_prop):
		for i in range(0, len(rows)):
			if rows[i][0] == chem_data['node']['smiles']:
				rows[i].insert(header_index, chem_data['data'][spec_prop]['smiles'])


	def parseToCSV(self, run_data):

		# logging.warning("RUN DATA: {}".format(run_data))

		jid = JchemCalc().gen_jid()  # create timestamp
		time_str = datetime.datetime.strptime(jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')

		response = HttpResponse(content_type='text/csv')
		content_disposition = ''

		if 'batch_data' in run_data:
			content_disposition = 'attachment; filename=' + self.model + '_batch_' + jid + '.csv'	
		else:
			content_disposition = 'attachment; filename=' + self.model + '_' + jid + '.csv'
			
		# Adds 'likely' to CSV filename if gentrans likely CSV:
		if run_data.get('csv_type') == "likely":
			parsed_string = content_disposition.split(jid)  # splits filename at jid
			content_disposition = parsed_string[0] + "likely_" + jid + parsed_string[1]  # adds 'likely' to filename

		if isinstance(run_data['run_data'], str):
			run_data['run_data'] = json.loads(run_data['run_data'])

		response['Content-Disposition'] = content_disposition

		logging.info("Beginning CSV parsing..")

		rows = []
		headers = []

		# Build rows for chemicals:
		if 'batch_data' in run_data:
			if 'workflow' in run_data and run_data['workflow'] == 'gentrans':
				for i in range(0, len(run_data['batch_data'])):
					parent_products = run_data['batch_data'][i]
					for j in range(0, len(parent_products)):
						rows.append([])
			else:
				for i in range(0, len(run_data['batch_chems'])):
					rows.append([])
		else:
			if 'workflow' in run_data and run_data['workflow'] == 'gentrans':
				for i in range(0, len(run_data['data'])):
					rows.append([])
			else:
				rows.append([])

		# Add molecular info header if gentrans:
		if run_data['workflow'] == 'gentrans':
			self.molecular_info = self.molecular_info + ['production', 'accumulation', 'globalAccumulation', 'likelihood']

			# TODO: Add QSAR here if it was selected as an option by the user
			# Will need to pass qsar selection from input to output



		# write parent info first and in order..
		for prop in self.molecular_info:

			if not 'batch_data' in run_data:

				if run_data['workflow'] == 'gentrans':
					headers.append(prop)
					i = 0
					for metabolite in run_data['data']:
						for key, val in metabolite.items():
							if key == prop and key not in rows[i]:
								rows[i].append(val)
								i += 1
				else:
					for key, val in run_data['run_data'].items():
						if key == prop:
							headers.append(key)
							rows[0].append(val)
			else:
				headers.append(prop)
				i = 0
				j = 0  # trying it here for gentrans batch mode!
				for chem_data in run_data['batch_chems']:

					if run_data['workflow'] == 'gentrans':
						for product in run_data['batch_data'][i]:
							data = product[prop]
							rows[j].append(data)
							j += 1
						i += 1

					else:
						data = chem_data[prop]
						rows[i].append(data)
						i += 1

		if self.model == 'chemspec':

			if 'run_type' in run_data and run_data['run_type'] == 'batch':

				for spec_prop in self.speciation_props:
					for chem_data in run_data['batch_data']:

						if spec_prop == 'isoelectricPoint':
							header = "isoelectric point"
							if not header in headers:
								headers.append(header)

							header_index = headers.index(header)

							for i in range(0, len(rows)):
								if rows[i][0] == chem_data['node']['smiles']:
									rows[i].insert(header_index, chem_data['data'][spec_prop])

						elif spec_prop == 'pka' or spec_prop == 'pkb':
							j = 1
							for item in chem_data['data'][spec_prop]:
								header = "pka_{}".format(j)
								j += 1
								if not header in headers:
									headers.append(header)
									for n in range(0, len(rows)):
										rows[n].append("")
								header_index = headers.index(header)
								for n in range(0, len(rows)):
									if rows[n][0] == chem_data['node']['smiles']:
										rows[n].insert(header_index, item)

						elif spec_prop == 'majorMicrospecies':
							if not spec_prop in headers:
								headers.append(spec_prop)
							header_index = headers.index(spec_prop)
							self.insert_rows(rows, header_index, chem_data, spec_prop)

						elif spec_prop == 'pka-micospecies':
							j = 1
							for ms in chem_data['data'][spec_prop].items():
								header = "microspecies_{}".format(j)
								j += 1
								if not header in headers:
									headers.append(header)
								header_index = headers.index(header)
								self.insert_rows(rows, header_index, chem_data, spec_prop)
			else:
				run_data = run_data['run_data']
				for key, val in run_data.items():
					if key not in self.molecular_info:
						if key == 'isoelectricPoint':
							headers.append(key)
							rows[0].append(val)
						elif key == 'pka' or key == 'pkb':
							i = 0 # pka counter
							for item in val:
								headers.append(key + "_" + str(i))
								rows[0].append(item)
								i+=1
						elif key == 'majorMicrospecies':
							headers.append(key + '-smiles')
							rows[0].append(val['smiles'])
						elif key == 'pka-micospecies':
							for ms in val.items():
								# each ms is a jchem_structure object
								headers.append(key + '-smiles')
								rows[0].append(val['smiles'])
						elif key == 'tautomers':
							i = 0
							for item in val:
								headers.append(item['key'] + "_" + str(i))
								rows[0].append(item['smiles'])
								i+=1

		elif self.model == 'pchemprop':
			if 'batch_data' in run_data:

				multiChemPchemDataRowBuilder(headers, rows, self.props, run_data, self)

			else:
				for prop in self.props:
					for calc, calc_props in run_data['checkedCalcsAndProps'].items():
						if not prop in calc_props:
							continue

						if prop == "ion_con":
							for pka_key, pka_val in calc_props[prop].items():
								if pka_val and pka_val != 'none':
									pka_num = str(int(pka_key[-1:]))
									new_pka_key = pka_key[:-1] + "_" + pka_num
									headers.append("{} ({})".format(new_pka_key, calc))
									rows[0].append(roundData(prop, pka_val))
						elif '<br>' in calc_props.get(prop, ''):
							# calc-prop value has methods, e.g., "-1.102 (KLOP)<br>-1.522 (VG)<br>-1.344 (PHYS)<br>"
							method_data = calc_props[prop].split('<br>')
							method_data.remove('')  # remove trailing '' list item
							for method_datum in method_data:
								value = method_datum.split()[0]  # value, method
								method = method_datum.split()[1]
								rows[0].append(roundData(prop, value))
								if prop == 'kow_wph':
									prop = self.new_phkow_key
								headers.append("{} ({}, {})".format(prop, calc, method))
						else:
							rows[0].append(roundData(prop, calc_props[prop]))
							if prop == 'kow_wph':
									prop = self.new_phkow_key
							headers.append("{} ({})".format(prop, calc))

					# Adds geomean column for prop:
					propGeomean = get_geomean_for_prop(prop, run_data['geomeanDict'])
					if propGeomean:
						rows[0].append(propGeomean)
						headers.append("{} ({})".format(prop, "geomean"))


		elif self.model == 'gentrans':
			# TODO: class this, e.g., Metabolizer (jchem_rest)
			if 'batch_data' in run_data:
				metabolites_data = run_data['batch_data']
			else:
				metabolites_data = run_data['data']

			if not metabolites_data:
				return HttpResponse("Error building csv for metabolites.")

			headers.insert(0, 'genKey') # insert generation headers first
			headers.insert(1, 'routes')  # transformation pathway			

			if 'batch_data' in run_data:

				parent_index = 0
				products_index = 0
				all_chems_data = []  # single-level list of chem objects

				for batch_chem_products in metabolites_data:
					# metabolites_data --> list of batch_chems arrays, which are a list
					# of each batch_chem's products/metabolits..

					for product in batch_chem_products:
						genkey_index = headers.index('genKey')
						routes_index = headers.index('routes')

						# Increment parent genKey for batch (e.g., 2nd chemical in batch input file genkeys: 2, 2.1, 2.1.2, ...)
						full_genkey = product['genKey'].split(' ')  # split key by space (e.g., 'molecule 1' --> ['molecule', '1'])
						parent_key = int(full_genkey[1][:1])  # just the parent bit of the genkey
						remaining_genkey = full_genkey[1][1:]  # the rest of the genkey number
						new_genkey = "{} {}{}".format(full_genkey[0], parent_key + parent_index, remaining_genkey)
						product['genKey'] = new_genkey
						rows[products_index].insert(genkey_index, new_genkey)
						rows[products_index].insert(routes_index, product['routes'])  # insert trans pathway into rows
						all_chems_data.append(product)
						products_index += 1

					parent_index += 1

				if run_data.get('csv_type') == 'likely':
					# Adds column for 'number of major products' for each parent, if likely csv:
					for batch_chem_products in metabolites_data:
						headers, rows = add_likely_products_column(headers, rows, batch_chem_products)
						headers, rows = renumber_likely_products(headers, rows)  # renumbers likely product genKey
						headers, rows = remove_routes_column(headers, rows)
				else:
					# Build rows for all batch chems + products with one call
					pchempropsForMetabolites(headers, rows, self.props, run_data, all_chems_data, self)

			else:
				# inserts genKey into first column of batch chems csv:
				products_index = 0
				for metabolite in metabolites_data:
					genkey_index = headers.index('genKey')
					routes_index = headers.index('routes')
					if 'genKey' not in rows[products_index]:
						rows[products_index].insert(genkey_index, metabolite['genKey'])
						rows[products_index].insert(routes_index, metabolite['routes'])  # insert trans pathway into rows
						products_index += 1

				# Adds column for 'number of major products' for each parent, if likely csv:
				if run_data.get('csv_type') == 'likely':
					headers, rows = add_likely_products_column(headers, rows, metabolites_data)
					headers, rows = renumber_likely_products(headers, rows)  # renumbers likely product genKey
					headers, rows = remove_routes_column(headers, rows)
				else:
					pchempropsForMetabolites(headers, rows, self.props, run_data, metabolites_data, self)

				
		# check for encoding issues that are laid out in the commented
		# out conditional above.
		return some_streaming_csv_view(headers, rows, run_data, content_disposition)


class Echo(object):
	"""
	An object that implements just the write method of the file-like
	interface.
	"""
	def write(self, value):
		"""Write the value by returning it, instead of storing in a buffer"""
		return value

# def some_streaming_csv_view(request):
def some_streaming_csv_view(headers, rows, run_data, content_disposition):
	"""A view that streams a large CSV file"""

	logging.warning("About to stream the CSV..")
	rows.insert(0, headers)
	pseudo_buffer = Echo()
	writer = csv.writer(pseudo_buffer)
	logging.warning("Writer initiated..")
	response = StreamingHttpResponse((writer.writerow(row) for row in rows),
		content_type="text/csv")
	logging.warning("HTTP streaming response complete..")
	response['Content-Disposition'] = content_disposition
	return response

def getCalcMapKeys(calc):
	"""
	returns prop map of requested calculator
	"""
	if calc == 'chemaxon':
		return JchemCalc().propMap.keys()
	elif calc == 'epi':
		return EpiCalc().propMap.keys()
	elif calc == 'test':
		return TestWSCalc().propMap.keys()
	elif calc == 'sparc':
		return SparcCalc().propMap.keys()
	else:
		return None


def roundData(prop, datum):
	try:
		round_list = ['water_sol', 'vapor_press', 'mol_diss', 'mol_diss_air', 
						'henrys_law_con', 'water_sol_ph']
		if prop in round_list:
			rounded_datum = "{:.2E}".format(datum)
			return rounded_datum
		else:
			return round(float(datum), 2)
	except ValueError as err:
		return datum
	except TypeError as err:
		# Triggered when trying to round something that's not a number.
		return datum


def multiChemPchemDataRowBuilder(headers, rows, props, run_data, csv_obj):

	for prop in props:
		for calc, calc_props in run_data['checkedCalcsAndProps'].items():
			data = None
			if 'batch_data' in run_data:
				data = run_data['batch_data']
			elif 'data' in run_data:
				data = run_data['data']

			for chem_data in data:

				if chem_data['calc'] == calc and chem_data['prop'] == prop:

					if prop == 'ion_con':
						if not chem_data.get('data') or not 'pKa' in chem_data['data']:
							chem_data['data'] = {'pKa': []}
						j = 1
						for pka in chem_data.get('data', {}).get('pKa', {}):
							header = "pka_{} ({})".format(j, calc)
							j += 1
							if not header in headers:
								headers.append(header)
								for i in range(0, len(rows)):
									rows[i].append("")
							header_index = headers.index(header)
							for i in range(0, len(rows)):
								if rows[i][0] == chem_data['node']['smiles']:
									rows[i].insert(header_index, roundData(prop, pka))
					else:
						if chem_data.get('method', False):
							if prop == 'kow_wph':
								header = "{} ({}, {})".format(csv_obj.new_phkow_key, calc, chem_data['method'])	
							else:
								header = "{} ({}, {})".format(prop, calc, chem_data['method'])
						else:
							if prop == 'kow_wph':
								header = "{} ({})".format(csv_obj.new_phkow_key, calc)
							else:
								header = "{} ({})".format(prop, calc)
						if not header in headers:
							headers.append(header)
						header_index = headers.index(header)
						for i in range(0, len(rows)):

							if run_data['workflow'] == 'gentrans':
								chem_smiles = rows[i][2]  # smiles after genKey column
							else:
								chem_smiles = rows[i][0]

							# if chem_smiles == chem_data['node']['smiles'] and chem_data['data'] not in rows[i]:
							if chem_smiles == chem_data['node']['smiles']:
								# temporary error handling...
								if 'error' in chem_data:
									rows[i].insert(header_index, chem_data['data'])
								elif 'method' in chem_data:	
									rows[i].insert(header_index, roundData(prop, chem_data['data']))
								else:
									rows[i].insert(header_index, roundData(prop, chem_data['data']))

		headers, rows = add_geomean_for_batch_chems(run_data, data, headers, rows, prop)



def pchempropsForMetabolites(headers, rows, props, run_data, metabolites_data, csv_obj):
	"""
	Basically same as multiChemPchemDataRowBuilder, but just for
	gentrans workflow.
	TODO: Refactor to only one pchemprop function for any and all workflows
	"""

	# if not run_data['checkedCalcsAndProps']:
	# 		return False

	if run_data['checkedCalcsAndProps']:

		for prop in props:
			for calc, calc_props in run_data['checkedCalcsAndProps'].items():
				
				if not prop in calc_props:
					continue  # move on to next iteration..

				for chem_data in metabolites_data:

					if not 'pchemprops' in chem_data:
						continue  # move on to next iteration..

					for pchem in chem_data['pchemprops']:

						if pchem.get('prop') != prop or pchem.get('calc') != calc:
							continue  # move on to next iteration..

						if pchem['prop'] == "ion_con":
							j = 1
							if not pchem.get('data') or not 'pKa' in pchem['data']:
								pchem['data'] = {'pKa': []}
							for pka in pchem['data'].get('pKa', []):
								header = "pka_{} ({})".format(j, calc)
								j += 1
								if not header in headers:
									headers.append(header)
									for i in range(0, len(rows)):
										rows[i].append("")
								header_index = headers.index(header)
								for i in range(0, len(rows)):
									if rows[i][2] == chem_data['smiles']:
										rows[i][header_index] = roundData(prop, pka)

						else:

							if pchem.get('method'):
								if prop == 'kow_wph':
									header = "{} ({}, {})".format(csv_obj.new_phkow_key, calc, pchem['method'])	
								else:
									header = "{} ({}, {})".format(prop, calc, pchem['method'])
							else:
								if prop == 'kow_wph':
									header = "{} ({})".format(csv_obj.new_phkow_key, calc)
								else:
									header = "{} ({})".format(prop, calc)

							if not header in headers:
								headers.append(header)

							header_index = headers.index(header)

							for i in range(0, len(rows)):

								if run_data['workflow'] == 'gentrans':
									smiles_index = headers.index('smiles')
									chem_smiles = rows[i][smiles_index]  # smiles after genKey column
								else:
									chem_smiles = rows[i][0]

								if chem_smiles != chem_data.get('smiles') or pchem.get('prop') != prop or chem_data.get('genKey') != rows[i][0]:
									continue  # move on to next iteration..

								if 'error' in chem_data or 'error' in pchem:
									rows[i].insert(header_index, roundData(prop, pchem['data']))
								else:
					
									rows[i].insert(header_index, roundData(prop, pchem['data']))

			headers, rows = add_geomean_for_metabolites(run_data, metabolites_data, headers, rows, prop)

	logging.warning("INCLUDE RATES: {}".format(run_data.get('includeRates')))
	if run_data.get('includeRates') == True:
		headers, rows = add_half_life_column(headers, rows, metabolites_data)



def add_geomean_for_batch_chems(run_data, batch_chems, headers, rows, prop):
	"""
	Adds geomean column to end of a given p-chem property.
	"""

	if not 'geomeanDict' in run_data:
		return

	for smiles_key, chem_geomean in run_data['geomeanDict'].items():

		for prop_key, prop_geomean in run_data['geomeanDict'][smiles_key].items():

			if prop_key != prop:
				continue

			for i in range(0, len(rows)):

				if run_data['workflow'] == 'gentrans':
					chem_smiles = rows[i][2]  # smiles after genKey column
				else:
					chem_smiles = rows[i][0]

				if smiles_key != chem_smiles:
					continue

				# Adds geomean column for metabolite prop:
				propGeomean = get_geomean_for_prop(prop, run_data['geomeanDict'][chem_smiles])
				if prop == 'kow_wph':
					header = "{} ({})".format("d_ow", "geomean")
				else:
					header = "{} ({})".format(prop, "geomean")
				if propGeomean:
					if not header in headers:
						headers.append(header)
					header_index = headers.index(header)
					rows[i].insert(header_index, roundData(prop, propGeomean))
				elif header in headers:
					# Inserts blank data if there's a geomean for other metabolites but not chem_data
					header_index = headers.index(header)
					rows[i].insert(header_index, "N/A")

	return headers, rows
		



def add_geomean_for_metabolites(run_data, metabolites_data, headers, rows, prop):

	for chem_data in metabolites_data:

		if not 'pchemprops' in chem_data:
			continue  # move on to next iteration..

		if not 'geomeanDict' in chem_data:
			continue

		for i in range(0, len(rows)):

			if run_data['workflow'] == 'gentrans':
				chem_smiles = rows[i][2]  # smiles after genKey column
			else:
				chem_smiles = rows[i][0]

			if chem_smiles != chem_data.get('smiles') or chem_data.get('genKey') != rows[i][0]:
				continue  # move on to next iteration..

			# Adds geomean column for metabolite prop:
			propGeomean = get_geomean_for_prop(prop, chem_data.get('geomeanDict'))
			if prop == 'kow_wph':
				header = "{} ({})".format("d_ow", "geomean")
			else:
				header = "{} ({})".format(prop, "geomean")
			if propGeomean:
				if not header in headers:
					headers.append(header)
				header_index = headers.index(header)
				rows[i].insert(header_index, roundData(prop, propGeomean))
			elif header in headers:
				# Inserts blank data if there's a geomean for other metabolites but not chem_data
				header_index = headers.index(header)
				rows[i].insert(header_index, "N/A")

	return headers, rows





def get_geomean_for_prop(prop, geometricDict):
	"""
	Loops geomtric values and returns data for
	requested prop as a .
	"""
	if not geometricDict:
		return None

	for propName, propGeomean in geometricDict.items():

		# Accounts for prop name change for CSV files (d_ow -> kow_wph):
		if prop == "d_ow":
			prop = "kow_wph"

		# Continues loop until prop match:
		if prop != propName: continue

		# Returns None if prop's geomean is None:
		if not propGeomean: return None

		# Returns None for props that don't have a geomean:
		if propName == 'ion_con': return None

		# Returns matching geomean for requested prop:
		return propGeomean



def add_likely_products_column(headers, rows, metabolites_data):
	"""
	Adds 'number of major products' column, which
	is number of products a parent has with global
	accumulation great than 10%.
	"""
	major_products_header = "major_products"
	major_products_index = 1

	if not major_products_header in headers:
		headers.insert(major_products_index, major_products_header)

	parent_data = metabolites_data[0]  # assuming first object in list is parent of remaining items
	parent_genkey = parent_data['genKey']

	num_major_products = len(metabolites_data) - 1

	for row in rows:
		if row[0] == parent_genkey and len(row) == len(headers):
			row[major_products_index] = num_major_products
		elif row[0] == parent_genkey:
			row.insert(major_products_index, num_major_products)
		elif len(row) < len(headers):
			row.insert(major_products_index, "")

	return headers, rows



def remove_routes_column(headers, rows):
	"""
	Removes the 'routes' column from the likely CSV.
	"""
	if not 'routes' in headers:
		return headers, rows
	route_index = headers.index('routes')
	for row in rows:
		del row[route_index]
	del headers[route_index]
	return headers, rows



def renumber_likely_products(headers, rows):
	"""
	Renumbers likely product genkeys for the likely
	products CSV in the gentrans workflow. Currently, keeps
	parent genKey the same, and numbers its products with the
	following schema: 1-A, 1-B, etc.
	"""
	if not 'genKey' in headers:
		return headers, rows
	letter_id = "A"  # identifier for product (e.g., 1-A)
	prev_parent_num = None
	genkey_index = headers.index('genKey')
	for row in rows:
		genkey_val = row[0]  # gets parent or product genkey
		parent_num = genkey_val.split(" ")[1]  # splitting e.g., "molecule 1" to get number
		parent_num = parent_num.split(".")[0]  # gets parent value of molecule number
		if parent_num != prev_parent_num:
			letter_id = "A"  # resets letter back to "A" for new parent's products
			prev_parent_num = parent_num  # resets prev parent 
		if len(genkey_val.split(".")) > 1:
			# this is a product (i.e., "1.x..".split(".") > 1)
			new_genkey = "molecule {}-{}".format(parent_num, letter_id)
			row[0] = new_genkey
			letter_id = chr(ord(letter_id) + 1)  # increments letter
	return headers, rows



def add_half_life_column(headers, rows, metabolites_data):
	"""
	Adds half-life data to CSV. Inserts column after molecular info
	"""
	half_life_header = "Half life (days)"
	half_life_index = headers.index("likelihood") + 1

	headers.insert(half_life_index, half_life_header)

	# TODO: Convert all half-lives to days

	row_index = 0
	for row in rows:
		# Get metabolite data for given row:
		met_data = {}
		for data in metabolites_data:
			if data['genKey'] == row[0]:
				if data.get('qsar'):
					rows[row_index].insert(half_life_index, data['qsar']['data'])
				else:
					rows[row_index].insert(half_life_index,  "N/A")
		row_index += 1		

	return headers, rows
