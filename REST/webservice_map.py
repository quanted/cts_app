"""
Herein lies the map to the various calculators' queries.
It's organized by pchemprop field ID (e.g., melting_point, ion_con).
"""

def determineBaseUrl():
	"""
	Change base url depending on if cts is
	running on local or cgi 
	"""
	import os

	if 'CTS_TEST_SERVER_INTRANET' in os.environ:
		return os.environ['CTS_TEST_SERVER_INTRANET']
	else:
		return os.environ['CTS_TEST_SERVER']


baseUrl = determineBaseUrl()
# baseUrl = "http://a.ibdb.net/cts" # old

# p-chem properties by form field names 
props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 
		'mol_diss', 'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'kow_ph']

calculator = {

	'test': {
		'name': 'test',
		'methods': ['fda', 'hierarchical', 'group', 'neighbor'],
		'methodsResultKeys': {
			'fda': 'TESTFDA', 
			'hierarchical': 'TESTHierarchical', 
			'group': 'TESTGroupContribution', 
			# 'consensus': 'TESTConsensus', 
			'neighbor': 'TESTNearestNeighbor'},
		'url': baseUrl + '/test/test/calc',
		'props': {
			'melting_point': 'meltingPoint',
			'boiling_point': 'boilingPoint',
			'water_sol': 'waterSolubility',
			'vapor_press': 'vaporPressure',
			
			'meltingPoint': 'melting_point',
			'boilingPoint': 'boiling_point',
			'waterSolubility': 'water_sol',
			'vaporPressure':'vapor_press'
		}
	},

	'epi': {
		'name': 'epi',
		'methods': [''], # no methods for epi suite
		'url': baseUrl + '/test/epi/calc',
		'props': {
			'melting_point': 'meltingPtDegCEstimated',
			'boiling_point': 'boilingPtDegCEstimated',
			'water_sol': 'waterSolMgLEstimated',
			'vapor_press': 'vaporPressMmHgEstimated',
			'henrys_law_con': 'henryLcBondAtmM3Mole',
			'kow_no_ph': 'logKowEstimate',

			'meltingPtDegCEstimated': 'melting_point',
			'boilingPtDegCEstimated': 'boiling_point',
			'waterSolMgLEstimated': 'water_sol',
			'vaporPressMmHgEstimated': 'vapor_press',
			'henryLcBondAtmM3Mole': 'henrys_law_con',
			'logKowEstimate': 'kow_no_ph'
		}
	},

	# 'measured': {
	# 	'name': 'measured',
	# 	'methods': [''],
	# 	'url': baseUrl + '/test/measured',
	# 	'props': {
	# 		'melting_point': 'meltingPoint',
	# 		'boiling_point': 'boilingPoint',
	# 		'water_sol': 'waterSolubility',
	# 		'vapor_press': 'vaporPressure',
			
	# 		'meltingPoint': 'melting_point',
	# 		'boilingPoint': 'boiling_point',
	# 		'waterSolubility': 'water_sol',
	# 		'vaporPressure':'vapor_press'
	# 	}
	# }

}
