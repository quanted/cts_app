from django.views.decorators.http import require_POST

@require_POST
def chemspecOutputPage(request):
    import chemspec_model

    chemStruct = request.POST.get('chem_struct')
    pKaDecs = request.POST.get('pKa_decimals')
    pKaPhLow = request.POST.get('pKa_pH_lower')
    pKaPhUp = request.POST.get('pKa_pH_upper')
    pKaPhInc = request.POST.get('pKa_pH_increment')
    phMicroSpec = request.POST.get('pH_microspecies')
    isoElectPtPhInc = request.POST.get('isoelectricPoint_pH_increment')
    tautMaxNumStructs = request.POST.get('tautomer_maxNoOfStructures')
    tautMaxNumStructsPh = request.POST.get('tautomer_maxNoOfStructures_pH')
    sterMaxNumStructs = request.POST.get('stereoisomers_maxNoOfStructures')

    chemspec_obj = chemspec_model.chemspec("single", chemStruct, pKaDecs, pKaPhLow, pKaPhUp, pKaPhInc, phMicroSpec, isoElectPtPhInc, 
                    tautMaxNumStructs, tautMaxNumStructsPh, sterMaxNumStructs)

    return chemspec_obj