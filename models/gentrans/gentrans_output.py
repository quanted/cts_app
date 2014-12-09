from django.views.decorators.http import require_POST
import logging

@require_POST
def gentransOutputPage(request):
    import gentrans_model

    chemStruct = request.POST.get('chem_struct')
    smiles = request.POST.get('smiles')
    name = request.POST.get('name')
    formula = request.POST.get('formula')
    mass = request.POST.get('mass')
    
    abioticHydrolysis = request.POST.get('abiotic_hydrolysis')
    abioticRecuction = request.POST.get('abiotic_reduction')
    mammMetabolism = request.POST.get('mamm_metabolism')
    genLimit = request.POST.get('gen_limit')
    popLimit = request.POST.get('pop_limit')
    likelyLimit = request.POST.get('likely_limit')

    gentrans_obj = gentrans_model.gentrans("single", chemStruct, smiles, name, formula, 
                                    mass, abioticHydrolysis, abioticRecuction,
                                    mammMetabolism, genLimit, popLimit, likelyLimit)

    return gentrans_obj