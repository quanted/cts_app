from django.views.decorators.http import require_POST
import logging

@require_POST
def gentransOutputPage(request):
    import gentrans_model

    chemStruct = request.POST.get('chem_struct')
    abioticHydrolysis = request.POST.get('abiotic_hydrolysis')
    abioticRecuction = request.POST.get('abiotic_reduction')
    mammMetabolism = request.POST.get('mamm_metabolism')
    genLimit = request.POST.get('gen_limit')
    popLimit = request.POST.get('pop_limit')
    likelyLimit = request.POST.get('likely_limit')

    logging.warning("OUTPUT: " + str(genLimit))

    gentrans_obj = gentrans_model.gentrans("single", chemStruct, abioticHydrolysis, abioticRecuction,
                                    mammMetabolism, genLimit, popLimit, likelyLimit)

    return gentrans_obj