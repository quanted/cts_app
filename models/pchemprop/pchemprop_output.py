from django.views.decorators.http import require_POST
from . import pchemprop_model
import bleach
import logging


@require_POST
def pchempropOutputPage(request, metabolite=False):

    # NOTE: Adding metabolite input for gathering p-chem properties
    # for metabolites on the gentrans output page...

    if metabolite:
        pchemprop_obj = pchemprop_model.PChemProp('metabolite')
    else:
        pchemprop_obj = pchemprop_model.PChemProp('single')

    # Chemical from Chemical Editor
    pchemprop_obj.chem_struct = bleach.clean(request.POST.get('chem_struct', ''))

    pchemprop_obj.smiles = bleach.clean(request.POST.get('smiles', ''))   

    # pchemprop_obj.iupac = bleach.clean(request.POST.get('iupac', ''))
    pchemprop_obj.name = bleach.clean(request.POST.get('iupac', ''))
    pchemprop_obj.formula = bleach.clean(request.POST.get('formula', ''))
    pchemprop_obj.mass = bleach.clean(request.POST.get('mass', ''))
    pchemprop_obj.orig_smiles = bleach.clean(request.POST.get('orig_smiles', ''))
    pchemprop_obj.exactMass = bleach.clean(request.POST.get('exactmass', ''))
    pchemprop_obj.cas = bleach.clean(request.POST.get('cas', ''))

    pchemprop_obj.preferredName = bleach.clean(request.POST.get('preferredName', ''))
    pchemprop_obj.casrn = bleach.clean(request.POST.get('casrn', ''))
    pchemprop_obj.dtxsid = bleach.clean(request.POST.get('dtxsid', ''))

    # Pchem Properties Column Checkboxes
    pchemprop_obj.chemaxon = bleach.clean(request.POST.get('chemaxon', ''))
    pchemprop_obj.test = bleach.clean(request.POST.get('test', ''))
    pchemprop_obj.epi = bleach.clean(request.POST.get('epi', ''))
    # pchemprop_obj.sparc = bleach.clean(request.POST.get('sparc', ''))
    pchemprop_obj.equation = bleach.clean(request.POST.get('equation', ''))
    pchemprop_obj.measured = bleach.clean(request.POST.get('measured', ''))
    pchemprop_obj.opera = bleach.clean(request.POST.get('opera', ''))

    # Pchem Properties Table Checkboxes
    pchemprop_obj.melting_point = bleach.clean(request.POST.get('melting_point', ''))
    pchemprop_obj.boiling_point = bleach.clean(request.POST.get('boiling_point', ''))
    pchemprop_obj.water_sol = bleach.clean(request.POST.get('water_sol', ''))
    pchemprop_obj.water_sol_ph = bleach.clean(request.POST.get('water_sol_ph', ''))
    pchemprop_obj.vapor_press = bleach.clean(request.POST.get('vapor_press', ''))
    pchemprop_obj.mol_diss = bleach.clean(request.POST.get('mol_diss', ''))
    pchemprop_obj.mol_diss_air = bleach.clean(request.POST.get('mol_diss_air', ''))
    pchemprop_obj.ion_con = bleach.clean(request.POST.get('ion_con', ''))
    pchemprop_obj.henrys_law_con = bleach.clean(request.POST.get('henrys_law_con', ''))
    pchemprop_obj.kow_no_ph = bleach.clean(request.POST.get('kow_no_ph', ''))
    pchemprop_obj.kow_wph = bleach.clean(request.POST.get('kow_wph', ''))
    pchemprop_obj.kow_ph = bleach.clean(request.POST.get('kow_ph', ''))
    pchemprop_obj.koc = bleach.clean(request.POST.get('koc', ''))
    pchemprop_obj.log_bcf = bleach.clean(request.POST.get('log_bcf', ''))
    pchemprop_obj.log_baf = bleach.clean(request.POST.get('log_baf', ''))

    pchemprop_obj.fillCalcsandPropsDict()

    return pchemprop_obj