from django.views.decorators.http import require_POST
from django.utils.encoding import smart_text
import logging

@require_POST
def chemspecOutputPage(request):
    import chemspec_model

    # Chemical Editor tab
    chemStruct = request.POST.get('chem_struct')
    smiles = request.POST.get('smiles')
    name = request.POST.get('name')
    formula = request.POST.get('formula')
    mass = request.POST.get('mass')

    # Checmial Speciation tab - checkboxes
    pkaChkbox = request.POST.get('pka_chkbox', 'off')
    tautChkbox = request.POST.get('tautomer_chkbox', 'off')
    stereoChkbox = request.POST.get('stereoisomer_chkbox', 'off')

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

    chemspec_obj = chemspec_model.chemspec("single", chemStruct, smiles, name, formula, 
                    mass, pkaChkbox, tautChkbox, stereoChkbox, pKaDecs, pKaPhLow, 
                    pKaPhUp, pKaPhInc, phMicroSpec, isoElectPtPhInc, 
                    tautMaxNumStructs, tautMaxNumStructsPh, sterMaxNumStructs)

    return chemspec_obj