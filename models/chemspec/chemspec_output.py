from django.views.decorators.http import require_POST
from django.utils.encoding import smart_text
import logging

@require_POST
def chemspecOutputPage(request):
    import chemspec_model

    # Chemical Editor tab
    chemStruct = request.POST.get('chem_struct')
    smiles = request.POST.get('smiles')
    orig_smiles = request.POST.get('orig_smiles')
    name = request.POST.get('iupac')
    formula = request.POST.get('formula')
    mass = request.POST.get('mass')

    # Checmial Speciation tab - checkboxes
    get_pka = request.POST.get('get_pka')
    get_taut = request.POST.get('get_taut')
    get_stereo = request.POST.get('get_stereo')

    # Checmial Speciation tab - inputs 
    pKaDecs = request.POST.get('pKa_decimals')
    pKaPhLow = request.POST.get('pKa_pH_lower')
    pKaPhUp = request.POST.get('pKa_pH_upper')
    pKaPhInc = request.POST.get('pKa_pH_increment')
    phMicroSpec = request.POST.get('pH_microspecies')
    isoElectPtPhInc = request.POST.get('isoelectricPoint_pH_increment')

    tautMaxNumStructs = request.POST.get('tautomer_maxNoOfStructures')
    tautMaxNumStructsPh = request.POST.get('tautomer_pH')
    
    sterMaxNumStructs = request.POST.get('stereoisomers_maxNoOfStructures')

    chemspec_obj = chemspec_model.chemspec(chemStruct, smiles, orig_smiles, name, formula, 
                    mass, get_pka, get_taut, get_stereo, pKaDecs, pKaPhLow, 
                    pKaPhUp, pKaPhInc, phMicroSpec, isoElectPtPhInc, 
                    tautMaxNumStructs, tautMaxNumStructsPh, sterMaxNumStructs)

    return chemspec_obj