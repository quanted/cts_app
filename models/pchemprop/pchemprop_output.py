from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
import logging

@require_POST
def pchempropOutputPage(request):
    # return "test" 
    import pchemprop_model

    # Chemical from Chemical Editor
    chemStruct = request.POST.get('chem_struct')
    smiles = request.POST.get('smiles')
    name = request.POST.get('name')
    formula = request.POST.get('formula')
    mass = request.POST.get('mass')

    # Pchem Properties Column Checkboxes
    chemaxon = request.POST.get('chemaxon')
    test = request.POST.get('test')
    epi = request.POST.get('epi')
    sparc = request.POST.get('sparc')
    # measured = request.POST.get('measured') # now "average", which is computed

    # Pchem Properties Table Checkboxes
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

    # dataDict = {}
    # for key, value in request.POST.items():
    #     logging.info("{}: {}".format(key, value))

    pchemprop_obj = pchemprop_model.pchemprop("single", chemStruct, smiles, name, formula, 
                        mass, chemaxon, epi, test, sparc, meltingPoint, boilingPoint, 
                        waterSol, vaporPress, molDiss, ionCon, henrysLawCon, kowNoPh, kowWph, 
                        kowPh, koc)

    # pchemprop_obj = pchemprop_model.pchemprop(None)

    return pchemprop_obj


