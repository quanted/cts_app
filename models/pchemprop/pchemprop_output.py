from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
import logging

@require_POST
def pchempropOutputPage(request):
<<<<<<< Updated upstream
    import pchemprop_model
=======
>>>>>>> Stashed changes

    # return "test" 
    import pchemprop_model

    # Chemical from Chemical Editor
    chemStruct = request.POST.get('chem_struct')

    # Pchem Properties Column Checkboxes
    chemaxon = request.POST.get('chemaxon')
    epi = request.POST.get('epi')
    test = request.POST.get('test')
    sparc = request.POST.get('sparc')
    measured = request.POST.get('measured')

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

    pchemprop_obj = pchemprop_model.pchemprop("single", chemStruct, chemaxon, epi, test, sparc,
                        measured, meltingPoint, boilingPoint, waterSol, vaporPress, molDiss, 
                        ionCon, henrysLawCon, kowNoPh, kowWph, kowPh, koc)

    return pchemprop_obj


