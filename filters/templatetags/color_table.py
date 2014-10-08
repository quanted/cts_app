from django import template
import logging

register = template.Library()

# List of properties for p-chem calculator:
props_list = ['melting_point', 'boiling_point', 'water_sol', 'vapor_press', 'mol_diss', 
				'ionization_con', 'henrys_law_con', 'kow', 'koc', 'dist_coeff']

# List of each provider's available properties (see props list):
chemaxon_props = ['ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable', 'ChemCalcs_available', 
					'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available']

epi_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available']

test_props = ['ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable',
 				'ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_unavailable']

sparc_props = ['ChemCalcs_unavailable', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_available', 
				'ChemCalcs_available', 'ChemCalcs_available', 'ChemCalcs_unavailable', 'ChemCalcs_available']


# value - chemical property (melting point, etc)
# args - data source (e.g., chemaxon)
@register.filter(name='color_filter')
def color_filter(value, args):
	

	service_props = []

	if args == 'chemaxon':
		service_props = chemaxon_props
	elif args == 'epi':
		service_props = epi_props
	elif args == 'test':
		service_props = test_props
	elif args == 'sparc':
		service_props = sparc_props

	gen_dict = dict(zip(props_list, service_props)) # Make key/value pairs out of props list and service list
	# logging.warning("prop:" + prop)
	logging.warning("value:" + str(value.name))
	return gen_dict[value.name]
	# logging.warning(str(gen_dict[prop]))