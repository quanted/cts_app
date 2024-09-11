import logging

from django.views.decorators.http import require_POST
from . import chemspec_model
import bleach

@require_POST
def chemspecOutputPage(request):

    run_type = request.POST.get('run_type')

    # Chemical Editor tab
    chemStruct = bleach.clean(request.POST.get('chem_struct', ''))
    smiles = bleach.clean(request.POST.get('smiles', ''))
    orig_smiles = bleach.clean(request.POST.get('orig_smiles', ''))
    iupac = bleach.clean(request.POST.get('iupac', ''))
    formula = bleach.clean(request.POST.get('formula', ''))
    cas = bleach.clean(request.POST.get('cas', ''))
    mass = bleach.clean(request.POST.get('mass', ''))
    exact_mass = bleach.clean(request.POST.get('exactmass', ''))

    preferredName = bleach.clean(request.POST.get('preferredName', ''))
    casrn = bleach.clean(request.POST.get('casrn', ''))
    dtxsid = bleach.clean(request.POST.get('dtxsid', ''))

    # Checmial Speciation tab - checkboxes
    get_pka = bleach.clean(request.POST.get('get_pka', ''))
    get_taut = bleach.clean(request.POST.get('get_taut', ''))
    get_stereo = bleach.clean(request.POST.get('get_stereo', ''))

    # Checmial Speciation tab - inputs 
    pKaDecs = bleach.clean(request.POST.get('pKa_decimals', ''))
    pKaPhLow = bleach.clean(request.POST.get('pKa_pH_lower', ''))
    pKaPhUp = bleach.clean(request.POST.get('pKa_pH_upper', ''))
    pKaPhInc = bleach.clean(request.POST.get('pKa_pH_increment', ''))
    phMicroSpec = bleach.clean(request.POST.get('pH_microspecies', ''))
    isoElectPtPhInc = bleach.clean(request.POST.get('isoelectricPoint_pH_increment', ''))

    tautMaxNumStructs = bleach.clean(request.POST.get('tautomer_maxNoOfStructures', ''))
    tautMaxNumStructsPh = bleach.clean(request.POST.get('tautomer_pH', ''))
    
    sterMaxNumStructs = bleach.clean(request.POST.get('stereoisomers_maxNoOfStructures', ''))

    chemspec_obj = chemspec_model.chemspec(run_type, chemStruct, smiles, orig_smiles, preferredName, iupac, formula, 
                    casrn, cas, dtxsid, mass, exact_mass, get_pka, get_taut, get_stereo, pKaDecs, pKaPhLow, 
                    pKaPhUp, pKaPhInc, phMicroSpec, isoElectPtPhInc, 
                    tautMaxNumStructs, tautMaxNumStructsPh, sterMaxNumStructs)

    return chemspec_obj