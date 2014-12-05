"""
2014-08-13 (np)
"""

import json
import requests
import gentrans_parameters # Chemical Speciation parameters
from REST import jchem_rest
import logging
from django.http import HttpRequest
import data_walks 

baseUrl = 'http://pnnl.cloudapp.net/efsws/rest/'

headers = {'Content-Type' : 'application/json'}


class gentrans(object):
	def __init__(self, run_type, chem_struct, abiotic_hydrolysis, abiotic_reduction, mamm_metabolism, gen_limit, pop_limit, likely_limit):

		self.jid = jchem_rest.gen_jid() # get time of run
		self.run_type = run_type # single or batch
		self.chem_struct = chem_struct # chemical structure

		#Reaction Libraries
		self.abiotic_hydrolysis = abiotic_hydrolysis # values: on or None
		self.abiotic_reduction = abiotic_reduction
		self.mamm_metabolism = mamm_metabolism

		self.gen_limit = gen_limit # generation limit
		self.pop_limit = pop_limit # population limit
		self.likely_limit = likely_limit

		# Known keys for metabolizer on pnnl server (11-5-14)
		metabolizerList = ["hydrolysis","abiotic_reduction", "human_biotransformation"]

		reactionLibs = {
			"hydrolysis": self.abiotic_hydrolysis,
			"abiotic_reduction": self.abiotic_reduction,
			"human_biotransformation": self.mamm_metabolism
		}

		self.trans_libs = []
		for key,value in reactionLibs.items():
			if value:
				self.trans_libs.append(key)

		dataDict = {
			'structure': self.chem_struct,
			'generationLimit': self.gen_limit,
			'populationLimit': self.pop_limit,
			'likelyLimit': self.likely_limit,
			'transformationLibraries': self.trans_libs,
			'excludeCondition': ""
			# 'generateImages': False
		}

		request = HttpRequest()
		request.POST = dataDict
		response = jchem_rest.getTransProducts(request)

		# fileout = open('C:\\Documents and Settings\\npope\\Desktop\\out.txt', 'w')
		# fileout.write(response.content)
		# fileout.close()

		# reformat data for outputting to tree structure:
		data_walks.metID = 0
		self.results = data_walks.recursive(response.content)

		self.rawData = response.content