from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
import logging

@require_POST
def pchempropOutputPage(request, metabolite=False):

    import pchemprop_model

    # NOTE: Adding metabolite input for gathering p-chem properties
    # for metabolites on the gentrans output page...

    if metabolite:
        pchemprop_obj = pchemprop_model.PChemProp('metabolite')
    else:
        pchemprop_obj = pchemprop_model.PChemProp('single')

    # Chemical from Chemical Editor
    pchemprop_obj.chem_struct = request.POST.get('chem_struct')

    pchemprop_obj.smiles = request.POST.get('smiles')
    pchemprop_obj.name = request.POST.get('name')
    pchemprop_obj.formula = request.POST.get('formula')
    pchemprop_obj.mass = request.POST.get('mass')
    pchemprop_obj.mass += " g/mol"



    # Pchem Properties Column Checkboxes
    pchemprop_obj.chemaxon = request.POST.get('chemaxon')
    pchemprop_obj.test = request.POST.get('test')
    pchemprop_obj.epi = request.POST.get('epi')
    pchemprop_obj.sparc = request.POST.get('sparc')
    pchemprop_obj.measured = request.POST.get('measured')
    # measured = request.POST.get('measured') # now "average", which is computed

    # Pchem Properties Table Checkboxes
    pchemprop_obj.melting_point = request.POST.get('melting_point')
    pchemprop_obj.boiling_point = request.POST.get('boiling_point')
    pchemprop_obj.water_sol = request.POST.get('water_sol')
    pchemprop_obj.vapor_press = request.POST.get('vapor_press')
    pchemprop_obj.mol_diss = request.POST.get('mol_diss')
    pchemprop_obj.ion_con = request.POST.get('ion_con')
    pchemprop_obj.henrys_law_con = request.POST.get('henrys_law_con')
    pchemprop_obj.kow_no_ph = request.POST.get('kow_no_ph')
    pchemprop_obj.kow_wph = request.POST.get('kow_wph')
    pchemprop_obj.kow_ph = request.POST.get('kow_ph')
    pchemprop_obj.koc = request.POST.get('koc')

    pchemprop_obj.fillCalcsandPropsDict()

    # dataDict = {}
    # for key, value in request.POST.items():
    #     logging.info("{}: {}".format(key, value))

    #pchemprop_obj = pchemprop_model.PChemProp("single", chemStruct, smiles, name, formula,
    #                    mass, chemaxon, epi, test, sparc, measured, meltingPoint, boilingPoint,
    #                    waterSol, vaporPress, molDiss, ionCon, henrysLawCon, kowNoPh, kowWph,
    #                    kowPh, koc)

    # pchemprop_obj = pchemprop_model.pchemprop(None)

    return pchemprop_obj


