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


baseUrl = determineBaseUrl();
# baseUrl = "http://a.ibdb.net/cts" # old

# p-chem properties by form field names 
props = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 
		'mol_diss', 'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'kow_ph']

calculator = {

	'test': {
		'name': 'test',
		'methods': ['fda', 'hierarchical', 'group', 'consensus', 'neighbor'],
		'baseUrl': baseUrl + '/test/test/calc',
		'props': {
			'melting_point': 'meltingPoint',
			'boiling_point': 'boilingPoint',
			'water_sol': 'waterSolubility',
			'vapor_press': 'vaporPressure'
		}
	}

}

"""
Calculator:
  name 
  methods
  baseUrl
  propUrls
  props
"""

# def 
