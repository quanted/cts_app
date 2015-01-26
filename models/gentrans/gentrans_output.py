from django.views.decorators.http import require_POST
import logging

@require_POST
def gentransOutputPage(request):
    import gentrans_model
    from models.pchemprop import pchemprop_model

    # Chemical Editor tab fields
    chemStruct = request.POST.get('chem_struct')
    smiles = request.POST.get('smiles')
    name = request.POST.get('name')
    formula = request.POST.get('formula')
    mass = request.POST.get('mass')
    
    # Reaction Pathway Simulator tab fields
    abioticHydrolysis = request.POST.get('abiotic_hydrolysis')
    abioticRecuction = request.POST.get('abiotic_reduction')
    mammMetabolism = request.POST.get('mamm_metabolism')
    genLimit = request.POST.get('gen_limit')
    popLimit = request.POST.get('pop_limit')
    likelyLimit = request.POST.get('likely_limit')

    # Pchem Properties Column Checkboxes (p-chem prop tab fields)
    chemaxon = request.POST.get('chemaxon')
    test = request.POST.get('test')
    epi = request.POST.get('epi')
    sparc = request.POST.get('sparc')
    # measured = request.POST.get('measured') # now "average", which is computed

    # Pchem Properties Table Checkboxes (p-chem prop tab fields)
    meltingPoint = request.POST.get('melting_point')
    boilingPoint = request.POST.get('boiling_point')
    waterSol = request.POST.get('water_sol')
    vaporPress = request.POST.get('vapor_press')
    molDiss = request.POST.get('mol_diss')
    ionCon = request.POST.get('ion_con')
    henrysLawCon = request.POST.get('henrys_law_con')
    kowNoPh = request.POST.get('kow_no_ph')
    kowWph = request.POST.get('kow_wph')
    kowPh = request.POST.get('kow_ph')
    koc = request.POST.get('koc')

    # get pchemprop results for gentrans
    # gentransOutputPage.pchemprop_obj = pchemprop_model.pchemprop("single", chemStruct, smiles, name, formula, 
    #                     mass, chemaxon, epi, test, sparc, measured, meltingPoint, boilingPoint, 
    #                     waterSol, vaporPress, molDiss, ionCon, henrysLawCon, kowNoPh, kowWph, 
    #                     kowPh, koc)
    
    # NOTE: pchemprop_obj appended to gentrans_obj for computing pchemprops
    # for parent molecule on page submit event. metabolite pchemprops can be 
    # obtained on the UI via scripts within cts_gentrans_tree.html 
    # pchemprop_obj = pchemprop_model.pchemprop("single", chemStruct, smiles, name, formula, 
    #                     mass, chemaxon, epi, test, sparc, meltingPoint, boilingPoint, 
    #                     waterSol, vaporPress, molDiss, ionCon, henrysLawCon, kowNoPh, kowWph, 
    #                     kowPh, koc)

    # get gentrans results
    # gentrans_obj = gentrans_model.gentrans("single", chemStruct, smiles, name, formula, 
    #                                 mass, abioticHydrolysis, abioticRecuction,
    #                                 mammMetabolism, genLimit, popLimit, likelyLimit, pchemprop_obj)

    gentrans_obj = gentrans_model.gentrans("single", chemStruct, smiles, name, formula, 
                                    mass, abioticHydrolysis, abioticRecuction,
                                    mammMetabolism, genLimit, popLimit, likelyLimit)

    return gentrans_obj