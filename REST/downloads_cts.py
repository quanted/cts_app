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

from chemaxon_cts.jchem_rest import gen_jid
from chemaxon_cts.jchem_calculator import JchemProperty
from epi_cts.epi_calculator import EpiCalc
from test_cts.test_calculator import TestCalc
from sparc_cts.sparc_calculator import SparcCalc


class CSV(object):
	def __init__(self, model):
		self.models = ['chemspec', 'pchemprop', 'gentrans']
		self.calcs = ['chemaxon', 'epi', 'test', 'sparc']
		self.props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss',
					  'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'kow_ph', 'koc']
		if model and (model in self.models):
			self.model = model  # model name
		else:
			raise KeyError("Model - {} - not accepted..".format(model))
		self.molecular_info = ['smiles', 'iupac', 'formula', 'mass']  # original user sructure

	def parseToCSV(self, run_data):

		jid = gen_jid()  # create timestamp
		time_str = datetime.datetime.strptime(jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')

		response = HttpResponse(content_type='text/csv')

		if 'batch_data' in run_data:
			response['Content-Disposition'] = 'attachment; filename=' + self.model + '_batch_' + jid + '.csv'	
		else:
			response['Content-Disposition'] = 'attachment; filename=' + self.model + '_' + jid + '.csv'

		writer = csv.writer(response)  # bind writer to http response

		# build title section of csv..
		writer.writerow([run_data['run_data']['title']])
		writer.writerow([run_data['run_data']['time']])
		writer.writerow([""])

		rows = []
		headers = []

		if 'batch_data' in run_data:
			for i in range(0, len(run_data['batch_chems'])):
				rows.append([])
		else:
			rows.append([])

		# write parent info first and in order..
		for prop in self.molecular_info:

			if not 'batch_data' in run_data:
				for key, val in run_data['run_data'].items():
					if key == prop:
						headers.append(key)
						rows[0].append(val)
			else:
				headers.append(prop)
				i = 0
				# for chem_data in run_data['batch_data']:
				for chem_data in run_data['batch_chems']:
					# fill out all the batch chemicals' molecular info..
					# data = chem_data['node'][prop]
					data = chem_data[prop]
					rows[i].append(data)
					i += 1


		if self.model == 'chemspec':
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
					# elif key == 'stereoisomers' or key == 'tautomers':
					elif key == 'tautomers':
						i = 0
						for item in val:
							headers.append(item['key'] + "_" + str(i))
							rows[0].append(item['smiles'])
							i+=1

		elif self.model == 'pchemprop':
			if 'batch_data' in run_data:
				# for calc, props in run_data['checkedCalcsAndProps'].items():
				for prop in self.props:
					for calc, props in run_data['checkedCalcsAndProps'].items():
						for chem_data in run_data['batch_data']:
							if chem_data['calc'] == calc and chem_data['prop'] == prop:
								# if calc == 'chemaxon' and prop == 'ion_con':
								if prop == 'ion_con':
									j = 1
									for pka in chem_data['data']['pKa']:
										# header = "{} (pka_{})".format(calc, j)
										header = "pka_{} ({})".format(j, calc)
										j += 1
										if not header in headers:
											headers.append(header)
											for i in range(0, len(rows)):
												rows[i].append("")
										header_index = headers.index(header)
										for i in range(0, len(rows)):
											if rows[i][0] == chem_data['node']['smiles']:
												rows[i].insert(header_index, pka)
								else:
									if 'method' in chem_data:
										header = "{} ({}, {})".format(prop, calc, chem_data['method'])
									else:
										header = "{} ({})".format(prop, calc)
									if not header in headers:
										headers.append(header)
									header_index = headers.index(header)
									for i in range(0, len(rows)):
										if rows[i][0] == chem_data['node']['smiles']:
											rows[i].insert(header_index, chem_data['data'])
			else:
				for prop in self.props:
					for calc, calc_props in run_data['checkedCalcsAndProps'].items():
						if prop in calc_props:
							if prop == "ion_con":
								for pka_key, pka_val in calc_props[prop].items():
									pka_num = str(int(pka_key[-1:]) + 1)
									new_pka_key = pka_key[:-1] + "_" + pka_num
									headers.append("{} ({})".format(new_pka_key, calc))
									rows[0].append(pka_val)
							elif calc == 'chemaxon' and prop == 'kow_no_ph' or calc == 'chemaxon' and prop == 'kow_wph':
								# e.g., "-1.102 (KLOP)<br>-1.522 (VG)<br>-1.344 (PHYS)<br>"
								method_data = calc_props[prop].split('<br>')
								method_data.remove('')  # remove trailing '' list item
								for method_datum in method_data:
									value = method_datum.split()[0]  # value, method
									method = method_datum.split()[1]
									headers.append("{} ({}, {})".format(prop, calc, method))
									rows[0].append(value)
							else:
								headers.append("{} ({})".format(prop, calc))
								rows[0].append(calc_props[prop])


		elif self.model == 'gentrans':
			# TODO: class this, e.g., Metabolizer (jchem_rest)
			metabolites_data = run_data['data']

			if not metabolites_data:
				return HttpResponse("error building csv for metabolites..")

			rows['headers'].insert(0, 'gen') # insert generation headers first

			met_pkas, met_pkbs = [], []
			# determine max # pkas for all metabolites, then create columns...
			for metabolite in metabolites_data:
				if 'pchemprops' in metabolite:
					for data_obj in metabolite['pchemprops']:
						if data_obj['prop'] == 'ion_con':
							try:
								met_pkas.append(len(data_obj['data']['pKa']))
								met_pkbs.append(len(data_obj['data']['pKb']))
							except TypeError:
								pass  # pKa and/or pKb is None, ignore..
							except KeyError:
								pass  # pKa and/or pKb is None, ignore..

			# build csv columns.. TODO: only build columns with props and calcs that are available!
			for prop in self.props:
				for calc in self.calcs:
					# only add header if prop exist for given calc..
					if prop in getCalcMapKeys(calc):
						if prop == 'ion_con':
							# build max pka and pkb columns..
							if len(met_pkas) > 0:
								for i in range (0, max(met_pkas)):
									col_header = "pKa_{} ({})".format(i, calc) # e.g., pka1 (chemaxon)
									rows['headers'].append(col_header)
							if len(met_pkbs) > 0:
								for i in range (0, max(met_pkbs)):
									col_header = "pKb_{} ({})".format(i, calc)
									rows['headers'].append(col_header)
						else:
							col_header = "{} ({})".format(prop, calc) # e.g., water_sol (epi)
							rows['headers'].append(col_header)
					# else:
					#     logging.info("{} not available for {}".format(prop, calc))

			# m = 1 # detabolite indexer
			logging.info("HEADERS: {}".format(rows['headers']))

			# list size out of whack because metabolites' gen, smiles, etc. isn't being declared,
			# just the props!!!!!

			gen_list = []

			# loop metabolite data, one per row, insert data at index of matching header:
			# (this builds the rows as list)
			for metabolite in metabolites_data:

				# predefine row because code below will insert data at index of its column header..
				new_row = [None]*len(rows['headers']) # todo: get this variable above, one time
				new_key = metabolite['genKey']
				rows[new_key] = new_row # add new row to rows object

				# logging.info(">>> NEW ROW: {}".format(new_key))
				gen_list.append(new_key)

				# insert metabolite gen key:value..
				header_index = rows['headers'].index('gen')
				rows[new_key][header_index] = metabolite['genKey']

				# insert metabolite smiles key:value..
				header_index = rows['headers'].index('smiles')
				rows[new_key][header_index] = metabolite['smiles']

				if 'pchemprops' in metabolite:
					for data_obj in metabolite['pchemprops']:

						calc, prop, data = data_obj['calc'], data_obj['prop'], data_obj['data']

						# insert data at index of matching header..
						if data_obj['prop'] == 'ion_con':
							for key, val in data.items():
								i = 0
								for pka in val:
									col_header = "{}{} ({})".format(key, i, calc)
									if col_header in rows['headers']:
										header_index = rows['headers'].index(col_header) # get index of col_header
										rows[new_key][header_index] = pka
									i+=1
						else:
							col_header = "{} ({})".format(prop, calc)
							if col_header in rows['headers']:
								header_index = rows['headers'].index(col_header)
								rows[new_key][header_index] = data

		# might have to add code to keep row order..
		# writer.writerow(rows['headers'])
		writer.writerow(headers)

		# todo: remove blank columns before writing to csv..
		# write data rows to csv file:
		if self.model == 'gentrans':
			for gen in gen_list: writer.writerow(rows[gen])
		else:
			for row in rows:
				encoded_row_data = []
				for datum in row:
					if isinstance(datum, unicode): datum = datum.encode('utf8')
					encoded_row_data.append(datum)
				writer.writerow(encoded_row_data)
			# for row, row_data in rows.items():
			# 	# add checking for character encoding..
			# 	encoded_row_data = []
			# 	for datum in row_data:
			# 		if isinstance(datum, unicode): datum = datum.encode('utf8')
			# 		encoded_row_data.append(datum)
			# 	if row != "headers": writer.writerow(encoded_row_data)

		return response


def getCalcMapKeys(calc):
	"""
	returns prop map of requested calculator
	"""
	if calc == 'chemaxon':
		return JchemProperty().propMap.keys()
	elif calc == 'epi':
		return EpiCalc().propMap.keys()
	elif calc == 'test':
		return TestCalc().propMap.keys()
	elif calc == 'sparc':
		return SparcCalc().propMap.keys()
	else:
		return None