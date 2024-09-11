from django.views.decorators.http import require_POST
import logging
from . import gentrans_model
import bleach

@require_POST
def gentransOutputPage(request):

	run_type = bleach.clean(request.POST.get('run_type', ''))

	# Chemical Editor tab fields
	chemStruct = bleach.clean(request.POST.get('chem_struct', ''))
	smiles = bleach.clean(request.POST.get('smiles', ''))
	iupac = bleach.clean(request.POST.get('iupac', ''))
	formula = bleach.clean(request.POST.get('formula', ''))
	mass = bleach.clean(request.POST.get('mass', ''))
	orig_smiles = bleach.clean(request.POST.get('orig_smiles', ''))
	exact_mass = bleach.clean(request.POST.get('exactmass', ''))
	cas = bleach.clean(request.POST.get('cas', ''))

	preferredName = bleach.clean(request.POST.get('preferredName', ''))
    casrn = bleach.clean(request.POST.get('casrn', ''))
    dtxsid = bleach.clean(request.POST.get('dtxsid', ''))
	
	# Reaction Pathway Simulator tab fields
	abioticHydrolysis = bleach.clean(request.POST.get('abiotic_hydrolysis', ''))
	abioticRecuction = bleach.clean(request.POST.get('abiotic_reduction', ''))
	mammMetabolism = bleach.clean(request.POST.get('mamm_metabolism', ''))
	photolysis_unranked = bleach.clean(request.POST.get('photolysis_unranked', ''))
	photolysis_ranked = bleach.clean(request.POST.get('photolysis_ranked', ''))
	genLimit = request.POST.get('gen_limit')
	popLimit = request.POST.get('pop_limit')
	likelyLimit = request.POST.get('likely_limit')
	pfas_environmental = bleach.clean(request.POST.get('pfas_environmental', ''))
	pfas_metabolism = bleach.clean(request.POST.get('pfas_metabolism', ''))

	biotrans_metabolism = bleach.clean(request.POST.get('biotrans_metabolism', ''))
	biotrans_libs = bleach.clean(request.POST.get('biotrans_libs', ''))

	envipath_metabolism = bleach.clean(request.POST.get('envipath_metabolism', ''))

	include_rates = bleach.clean(request.POST.get('include_rates', ''))

	tree_type = bleach.clean(request.POST.get('tree_type', ''))

	gentrans_obj = gentrans_model.gentrans(run_type, chemStruct, smiles, orig_smiles, preferredName, iupac, formula, 
									mass, exact_mass, casrn, cas, dtxsid, abioticHydrolysis, abioticRecuction,
									mammMetabolism, photolysis_unranked, photolysis_ranked, 
									pfas_environmental, pfas_metabolism, genLimit, popLimit, 
									likelyLimit, biotrans_metabolism, biotrans_libs, envipath_metabolism,
									include_rates, tree_type)

	return gentrans_obj

