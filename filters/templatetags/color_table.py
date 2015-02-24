from django import template
import logging

register = template.Library()

# List of properties for p-chem calculator:
props_list = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss', 
				'ion_con', 'henrys_law_con', 'kow_no_ph', 'kow_wph', 'koc']

# List of each provider's available properties (see props list):
chemaxon_props = ['ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 
					'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable']

# NOTE: temporarily setting koc for epi to unavailable
epi_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']

# NOTE: temporarily setting kow_no_ph for test to unavailable
test_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
 				'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']

sparc_props = ['ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable']

# NOTE: temporarily setting kow_no_ph for test to unavailable
# measured_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
#  				'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']


# value - chemical property (melting point, etc)
# args - data source (e.g., chemaxon)
@register.filter(name='color_filter')
def color_filter(value, args):

	if value.name != "kow_ph":

		service_props = []

		if args == 'chemaxon':
			service_props = chemaxon_props
		elif args == 'epi':
			service_props = epi_props
		elif args == 'test':
			service_props = test_props
		elif args == 'sparc':
			service_props = sparc_props
		# elif args == 'measured':
		# 	service_props = measured_props

		gen_dict = dict(zip(props_list, service_props)) # Make key/value pairs out of props list and service list

		return gen_dict[value.name]
