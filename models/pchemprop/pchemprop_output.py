from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

@require_POST
def pchempropOutputPage(request):
    import pchemprop_model

    # chem_name = request.POST.get('chemical_name')
    # use = request.POST.get('Use')
    # formu_name = request.POST.get('Formulated_product_name')
    # a_i = request.POST.get('percent_ai')
    # a_i = float(a_i)/100
    # Application_type = request.POST.get('Application_type')
    # seed_crop = float(request.POST.get('seed_crop'))

    # trex2_obj = trex2_model.trex2("single", chem_name, use, formu_name, a_i, Application_type, seed_treatment_formulation_name, seed_crop, seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, rate_out, day_out,
    #               ld50_bird, lc50_bird, NOAEC_bird, NOAEL_bird, aw_bird_sm, aw_bird_md, aw_bird_lg, 
    #               Species_of_the_tested_bird_avian_ld50, Species_of_the_tested_bird_avian_lc50, Species_of_the_tested_bird_avian_NOAEC, Species_of_the_tested_bird_avian_NOAEL,
    #               tw_bird_ld50, tw_bird_lc50, tw_bird_NOAEC, tw_bird_NOAEL, x, ld50_mamm, lc50_mamm, NOAEC_mamm, NOAEL_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
    #               m_s_r_p)

    # return trex2_obj


