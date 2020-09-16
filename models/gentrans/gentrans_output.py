from django.views.decorators.http import require_POST
import logging
from . import gentrans_model

@require_POST
def gentransOutputPage(request):
    # from cts_app.models.pchemprop import pchemprop_model

    run_type = request.POST.get('run_type')

    # Chemical Editor tab fields
    chemStruct = request.POST.get('chem_struct')
    smiles = request.POST.get('smiles')
    iupac = request.POST.get('iupac')
    formula = request.POST.get('formula')
    mass = request.POST.get('mass')
    orig_smiles = request.POST.get('orig_smiles')
    exact_mass = request.POST.get('exactmass')
    cas = request.POST.get('cas')
    
    # Reaction Pathway Simulator tab fields
    abioticHydrolysis = request.POST.get('abiotic_hydrolysis')
    abioticRecuction = request.POST.get('abiotic_reduction')
    mammMetabolism = request.POST.get('mamm_metabolism')
    photolysis = request.POST.get('photolysis')
    genLimit = request.POST.get('gen_limit')
    popLimit = request.POST.get('pop_limit')
    likelyLimit = request.POST.get('likely_limit')
    pfas_environmental = request.POST.get('pfas_environmental')
    pfas_metabolism = request.POST.get('pfas_metabolism')

    biotrans_metabolism = request.POST.get('biotrans_metabolism')
    biotrans_libs = request.POST.get('biotrans_libs')

    gentrans_obj = gentrans_model.gentrans(run_type, chemStruct, smiles, orig_smiles, iupac, formula, 
                                    mass, exact_mass, cas, abioticHydrolysis, abioticRecuction,
                                    mammMetabolism, photolysis, pfas_environmental, pfas_metabolism,
                                    genLimit, popLimit, likelyLimit, biotrans_metabolism, biotrans_libs)

    return gentrans_obj