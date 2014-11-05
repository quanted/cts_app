from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
import logging

@require_POST
def pchempropOutputPage(request):
    import pchemprop_model

    chemStruct = request.POST.get('chem_struct')
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

    # Calculator Column Checkboxes
    chemaxon = request.POST.get('chemaxon')
    epi = request.POST.get('epi')
    test = request.POST.get('test')
    sparc = request.POST.get('sparc')
    measured = request.POST.get('measured')

    pchemprop_obj = pchemprop_model.pchemprop("single", chemStruct, meltingPoint, boilingPoint, waterSol,
                        vaporPress, molDiss, ionCon, henrysLawCon, kowNoPh, kowWph, kowPh)

    return pchemprop_obj


