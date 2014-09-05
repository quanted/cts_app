from django.views.decorators.http import require_POST

@require_POST
def gentransOutputPage(request):
    import gentrans_model

    pKaDecs = request.POST.get('pKa_decimals')
    pKaPhLow = request.POST.get('pKa_pH_lower')
    pKaPhUp = request.POST.get('pKa_pH_upper')
    pKaPhInc = request.POST.get('pKa_pH_increment')
    phMicroSpec = request.POST.get('pH_microspecies')
    isoElectPtPhInc = request.POST.get('isoelectricPoint_pH_increment')
    tautMaxNumStructs = request.POST.get('tautomer_maxNoOfStructures')
    tautMaxNumStructsPh = request.POST.get('tautomer_maxNoOfStructures_pH')
    sterMaxNumStructs = request.POST.get('stereoisomers_maxNoOfStructures')

    gentrans_obj = gentrans_model.gentrans("single", pKaDecs, pKaPhLow, pKaPhUp, pKaPhInc, phMicroSpec, isoElectPtPhInc, 
                    tautMaxNumStructs, tautMaxNumStructsPh, sterMaxNumStructs)

    return gentrans_obj