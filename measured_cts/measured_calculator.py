import requests
import json
import logging
import os
from REST.calculator import Calculator

headers = {'Content-Type': 'application/json'}


class MeasuredCalc(Calculator):
	"""
	Measured Calculator
	A single URL call returns data
	for all the properties: melting point,
	boiling point, vapor pressure, water solubility,
	log_kow, and henry's law constant
	"""

	def __init__(self):
		Calculator.__init__(self)

		self.postData = {"smiles" : ""}
		self.name = "measured"
		self.baseUrl = os.environ['CTS_EPI_SERVER']
		self.urlStruct = "/episuiteapi/rest/episuite/measured"  # new way
		# self.urlStruct = "/rest/episuite/measured"  # old way

		# map workflow parameters to test
		self.propMap = {
			'melting_point': {
			   'result_key': 'melting_point'
			},
			'boiling_point': {
			   'result_key': 'boiling_point'
			},
			'water_sol': {
			   'result_key': 'water_solubility'
			},
			'vapor_press': {
			   'result_key': 'vapor_pressure'
			},
			'henrys_law_con': {
				'result_key': 'henrys_law_constant'
			},
			'kow_no_ph': {
				'result_key': 'log_kow'
			},
			'koc': {
				'result_key': 'log_koc'
			}
		}

		self.result_structure = {
			'structure': '',
			'propertyname': '',
			'propertyvalue': None
		}

	def getPostData(self):
		return {"structure": ""}

	def makeDataRequest(self, structure):
		
		post = self.getPostData()
		post['structure'] = structure
		url = self.baseUrl + self.urlStruct

		logging.info("Measured URL: {}".format(url))

		try:
			response = requests.post(url, data=json.dumps(post), headers=headers, timeout=30)
		except requests.exceptions.ConnectionError as ce:
			logging.info("connection exception: {}".format(ce))
			raise 
		except requests.exceptions.Timeout as te:
			logging.info("timeout exception: {}".format(te))
			raise 
		else:
			self.results = response
			return response

	def getPropertyValue(self, requested_property, response):
		"""
		Returns CTS data object for a requested
		property (cts format)
		"""
		# make sure property is in measured's format:
		if not requested_property in self.propMap.keys():
			# requested prop name doesn't match prop keys..
			raise KeyError(
				"requested property: {} for Measured data doesn't match Measured's property keys".format(
					requested_property))

		properties_dict = response['properties']
		data_obj = {
			'calc': "measured",
			'prop': requested_property
		}

		try:
			sparc_requested_property = self.propMap[requested_property]['result_key']

			if sparc_requested_property in properties_dict.keys():
				data_obj['data'] = properties_dict[sparc_requested_property]['propertyvalue']
			else:
				data_obj['data'] = "property not available".format(sparc_requested_property)

			return data_obj

		except Exception as err:
			logging.warning("Error at Measured Calc: {}".format(err))
			raise err


