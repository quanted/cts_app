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
from collections import defaultdict
from bs4 import BeautifulSoup

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


	### Pchem Workflow Functions: ##############################################################

	def get_pchem_values(self, calc_props, calc_name):
		"""
		Process pchem values for single run type
		"""
		values = defaultdict(dict)
		for prop, data in calc_props.items():
			if data == 'N/A':
				continue
				
			if '<br>' in str(data):
				data_points = data.split('<br>')
				for point in data_points:
					if not point:
						continue
					clean_point = BeautifulSoup(point, "html.parser").get_text()
					parts = clean_point.strip().split()
					if len(parts) >= 2:
						value = parts[0]
						method = parts[-1]
						key = f"{prop} ({calc_name}, {method})"
						values[key] = value
			else:
				if isinstance(data, str) and " " in data:
					parts = data.split()
					if len(parts) >= 2:
						for i in range(0, len(parts)-1, 2):
							value, method = parts[i], parts[i+1]
							key = f"{prop} ({calc_name}, {method})"
							values[key] = value
				else:
					key = f"{prop} ({calc_name})"
					values[key] = data
					
		return dict(values)

	def get_batch_pchem_values(self, batch_entries, calc_name):
		"""
		Process pchem values from batch data entries
		"""
		values = defaultdict(dict)
		
		for entry in batch_entries:
			if entry['calc'] != calc_name:
				continue
				
			prop = entry['prop']
			if 'method' in entry and entry['method']:
				key = f"{prop} ({calc_name}, {entry['method']})"
			else:
				key = f"{prop} ({calc_name})"
				
			values[key] = entry['data']
		
		return dict(values)

	def generate_pchemprop_rows(self, data):
		"""
		Generate rows for both single and batch run types.
		"""
		base_cols = ['smiles', 'formula', 'iupac', 'mass', 'exactMass']
		
		# Initialize column tracking
		pchem_cols = []
		temp_cols = defaultdict(list)
		
		if data.get('run_type') == 'batch':
			# Process batch data
			batch_data = data.get('batch_data', [])
			chemicals = data.get('batch_chems', [])
			
			# Group batch data by chemical
			chemical_data = defaultdict(list)
			for entry in batch_data:
				chemical = entry['chemical']
				chemical_data[chemical].append(entry)
			
			# Get all unique columns first
			for chemical, entries in chemical_data.items():
				for calc in set(entry['calc'] for entry in entries):
					calc_entries = [e for e in entries if e['calc'] == calc]
					pchem_vals = self.get_batch_pchem_values(calc_entries, calc)
					for key in pchem_vals:
						prop = key.split()[0]
						temp_cols[prop].append(key)
						
		else:
			# Process single chemical data
			for calc, props in data['checkedCalcsAndProps'].items():
				pchem_vals = self.get_pchem_values(props, calc)
				for key in pchem_vals:
					prop = key.split()[0]
					temp_cols[prop].append(key)
		
		# Sort columns by property order
		for prop in self.props:
			if prop in temp_cols:
				pchem_cols.extend(sorted(temp_cols[prop]))
		
		all_columns = base_cols + pchem_cols
		yield all_columns
		
		if data.get('run_type') == 'batch':
			# Generate rows for each chemical in batch
			for chem in data.get('batch_chems', []):
				row = {
					'smiles': chem['smiles'],
					'formula': chem['formula'],
					'iupac': chem['iupac'],
					'mass': chem['mass'],
					'exactMass': chem['exactMass']
				}
				
				# Get all pchem values for this chemical
				entries = chemical_data[chem['chemical']]
				for calc in set(entry['calc'] for entry in entries):
					calc_entries = [e for e in entries if e['calc'] == calc]
					row.update(self.get_batch_pchem_values(calc_entries, calc))
					
				yield [row.get(col, 'N/A') for col in all_columns]
				
		else:
			# Generate single row for single chemical
			run_data = data["run_data"]
			row = {
				'smiles': run_data['smiles'],
				'formula': run_data['formula'], 
				'iupac': run_data['name'],
				'mass': run_data['mass'],
				'exactMass': run_data['exactMass']
			}
			
			for calc, props in data['checkedCalcsAndProps'].items():
				row.update(self.get_pchem_values(props, calc))
				
			yield [row.get(col, 'N/A') for col in all_columns]

	def stream_pchemprop_csv(self, run_data, output_file):
		"""
		View function to stream chemical data as CSV.
		"""

		if "filename=" in output_file:
			output_file = output_file.split("filename=").pop()

		pseudo_buffer = Echo()
		writer = csv.writer(pseudo_buffer)
		response = StreamingHttpResponse(
			(writer.writerow(row) for row in self.generate_pchemprop_rows(run_data)),
			content_type="text/csv"
		)
		response['Content-Disposition'] = 'attachment; filename="{}"'.format(output_file)
		return response

	#############################################################################################




	### Gentrans Workflow Functions: ##############################################################

	def get_info_columns(self):
		return [
			'genKey', 'routes', 'smiles', 'iupac', 'formula', 'mass', 'exactMass',
			'preferredName', 'cas', 'production', 'accumulation', 'globalAccumulation',
			'likelihood'
		]

	def get_all_pchem_combinations(self, data):
		"""Extract and sort all property/calculator/method combinations."""
		property_order = {prop: idx for idx, prop in enumerate(self.props)}
		combinations = set()
		
		for molecule in data:
			for prop in molecule.get('pchemprops', []):
				method = prop['method'] if prop['method'] is not None else 'null'
				combinations.add((prop['prop'], prop['calc'], method))
		
		return sorted(
			combinations,
			key=lambda x: (
				property_order.get(x[0], float('inf')),
				x[1],
				x[2]
			)
		)

	def sort_by_genkey(self, molecule):
		"""Create sort key for genKey values."""
		parts = molecule['genKey'].replace('molecule ', '').split('.')
		return [int(x) if x.isdigit() else x for x in parts]

	def extract_molecule_pchem_values(self, molecule, pchem_combinations):
		"""Extract pchem values for a molecule."""
		values = {}
		
		# Initialize all combinations with N/A
		for prop, calc, method in pchem_combinations:
			column = f"{prop} ({calc}, {method})"
			values[column] = 'N/A'
		
		# Fill in available values
		for prop_data in molecule.get('pchemprops', []):
			method = prop_data['method'] if prop_data['method'] is not None else 'null'
			column = f"{prop_data['prop']} ({prop_data['calc']}, {method})"
			if column in values:
				values[column] = prop_data['data']
				
		return values

	def process_batch_data(self, data):
		"""Process batch data into unified format."""
		molecules = []
		
		# Each entry in batch_data corresponds to a chemical from batch_chems
		for idx, batch_molecules in enumerate(data['batch_data']):
			for molecule in batch_molecules:
				# Add batch index to genKey for uniqueness
				# molecule['genKey'] = f"batch_{idx+1}_{molecule['genKey']}"
				old_key = molecule['genKey'].split("molecule ")[-1]
				if "." not in old_key:
					new_key = f"molecule {idx + 1}"
				else:
					suffix = old_key.split(".", 1)[1]
					new_key = f"molecule {idx + 1}.{suffix}"
				molecule['genKey'] = new_key
				molecules.append(molecule)
		
		return molecules

	def process_single_data(self, data):
		"""Process single chemical data."""
		return data['data']

	def generate_gentrans_rows(self, data):
		"""Generate rows for CSV output."""
		# Determine if this is batch or single data
		is_batch = data.get('run_type') == 'batch'

		info_columns = self.get_info_columns()
		
		# Process data based on type
		if is_batch:
			molecules = self.process_batch_data(data)
		else:
			molecules = self.process_single_data(data)
			
		# Sort molecules
		molecules = sorted(molecules, key=self.sort_by_genkey)
		
		# Get property combinations and create column headers
		pchem_combinations = self.get_all_pchem_combinations(molecules)
		pchem_columns = [f"{prop} ({calc}, {method})" for prop, calc, method in pchem_combinations]
		all_columns = info_columns + pchem_columns
		
		# Yield header row
		yield all_columns
		
		# Yield data rows
		for molecule in molecules:
			row = {col: molecule.get(col, 'N/A') for col in info_columns}
			row.update(self.extract_molecule_pchem_values(molecule, pchem_combinations))
			yield [row[col] for col in all_columns]

	def stream_gentrans_csv(self, run_data, output_file):
		"""View function to stream chemical data as CSV."""

		if "filename=" in output_file:
			output_file = output_file.split("filename=").pop()

		pseudo_buffer = Echo()
		writer = csv.writer(pseudo_buffer)
		response = StreamingHttpResponse(
			(writer.writerow(row) for row in self.generate_gentrans_rows(run_data)),
			content_type="text/csv"
		)
		response['Content-Disposition'] = 'attachment; filename="{}"'.format(output_file)
		return response

#############################################################################################












	def insert_rows(self, rows, header_index, chem_data, spec_prop):
		for i in range(0, len(rows)):
			if rows[i][0] == chem_data['node']['smiles']:
				rows[i].insert(header_index, chem_data['data'][spec_prop]['smiles'])


	def parseToCSV(self, run_data):

		logging.warning("RUN DATA: {}".format(run_data))

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
			# NOTE: Only single mode for chemspec
			run_data = run_data['run_data']
			for key, val in run_data.items():
				if key not in self.molecular_info:
					if key == 'isoelectricPoint':
						headers.append(key)
						rows[0].append(val)
					elif key == 'pka' or key == 'pkb':
						for i, item in enumerate(val):
							headers.append("{}_{} (chemaxon)".format(key, i))
							rows[0].append(item)
					elif key in ["pkasolver", "molgpka", "measured"]:
						if not "data" in val or not "pka_list" in val.get("data"):
							continue
						for i, pka_val in enumerate(val["data"]["pka_list"]):
							headers.append("pka_{} ({})".format(i, key))
							rows[0].append(pka_val)
					elif key == 'majorMicrospecies':
						headers.append(key)
						rows[0].append(val['smiles'])
					elif key == 'pka_microspecies':
						logging.warning("pka_microspecies called!")
						for ms in val:
							headers.append(ms["key"])
							rows[0].append(ms["smiles"])
					elif key == 'tautomers':
						for i, item in enumerate(val):
							headers.append(item['key'] + "_" + str(i))
							rows[0].append(item['smiles'])

			return some_streaming_csv_view(headers, rows, run_data, content_disposition)

		elif self.model == 'pchemprop':

			###########################################################################
			# IMPORTANT: Big refactors for CSV downloads incoming. Currently have new
			# method for gentrans single, which needs batch mode tested as well.
			###########################################################################
			return self.stream_pchemprop_csv(run_data, content_disposition)

		elif self.model == 'gentrans':



			###########################################################################
			# IMPORTANT: Big refactors for CSV downloads incoming. Currently have new
			# method for gentrans single, which needs batch mode tested as well.
			###########################################################################
			return self.stream_gentrans_csv(run_data, content_disposition)

				
		# check for encoding issues that are laid out in the commented
		# out conditional above.
		# return some_streaming_csv_view(headers, rows, run_data, content_disposition)


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
