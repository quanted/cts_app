from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import HttpResponse
import importlib
import linksLeft
import logging


def outputPageView(request, model='none', header=''):

#     if(model == "pchemprop"):
# 	    html = render_to_string('01cts_uberheader.html', {'title': header+' Output'})
# 	    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'output'})
# 	    html = html + linksLeft.linksLeft()
# 	    html = html + render_to_string('04uberoutput_start.html', {
#             'model_attributes': header+' Output'})

# #	    html = html + modelOutputHTML
# 	    html = html + '''<table class="input_table tab tab_ChemCalcs" style="">
# <tbody><tr>
# <th></th>
# <th><input id="id_chemaxon_select" name="chemaxon" type="checkbox" class="col_header" value="true">ChemAxon</th>
# <th><input id="id_epi_select" name="epi" type="checkbox" class="col_header" value="true">EPI Suite</th>
# <th><input id="id_test_select" name="test" type="checkbox" class="col_header" value="true">TEST</th>
# <th><input id="id_sparc_select" name="sparc" type="checkbox" class="col_header" value="true">SPARC</th>
# <th><input id="id_measured_select" name="measured" type="checkbox" class="col_header" value="true">Measured</th>
# </tr>
# <tr>
# <th><input id="id_all" name="all" type="checkbox" value="true"><span>All</span></th>
# <td></td>
# <td></td>
# <td></td>
# <td></td>
# <td></td>
# </tr>




# <tr>
# <th class="chemprop"><input id="id_melting_point" name="melting_point" type="checkbox"> <span>Melting Point (C)</span></th>
# <td id="id_melting_point_ChemAxon" class="ChemCalcs_unavailable chemaxon id_melting_point" style="opacity: 1;"></td>
# <td id="id_melting_point_EPI" class="ChemCalcs_available epi id_melting_point" style="opacity: 0.75;"></td>
# <td id="id_melting_point_TEST" class="ChemCalcs_available test id_melting_point" style="opacity: 1;">-144.3</td>
# <td id="id_melting_point_SPARC" class="ChemCalcs_unavailable sparc id_melting_point" style="opacity: 0.75;"></td>
# <td id="id_melting_point_MEASURED" class="ChemCalcs_available measured id_melting_point" style="opacity: 1;">-138.2</td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_boiling_point" name="boiling_point" type="checkbox"> <span>Boiling Point (C)</span></th>
# <td id="id_boiling_point_ChemAxon" class="ChemCalcs_unavailable chemaxon id_boiling_point" style="opacity: 1;"></td>
# <td id="id_boiling_point_EPI" class="ChemCalcs_available epi id_boiling_point" style="opacity: 0.75;"></td>
# <td id="id_boiling_point_TEST" class="ChemCalcs_available test id_boiling_point" style="opacity: 1;">2.954</td>
# <td id="id_boiling_point_SPARC" class="ChemCalcs_available sparc id_boiling_point" style="opacity: 0.75;"></td>
# <td id="id_boiling_point_MEASURED" class="ChemCalcs_available measured id_boiling_point" style="opacity: 1;">-0.5000</td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_water_sol" name="water_sol" type="checkbox"> <span>Water Solubility (mg/L)</span></th>
# <td id="id_water_sol_ChemAxon" class="ChemCalcs_available chemaxon id_water_sol" style="opacity: 1;">-144.3</td>
# <td id="id_water_sol_EPI" class="ChemCalcs_available epi id_water_sol" style="opacity: 0.75;"></td>
# <td id="id_water_sol_TEST" class="ChemCalcs_available test id_water_sol" style="opacity: 1;">64.61</td>
# <td id="id_water_sol_SPARC" class="ChemCalcs_available sparc id_water_sol" style="opacity: 0.75;"></td>
# <td id="id_water_sol_MEASURED" class="ChemCalcs_available measured id_water_sol" style="opacity: 1;">61.16</td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_vapor_press" name="vapor_press" type="checkbox"> <span>Vapor Pressure (mmHg)</span></th>
# <td id="id_vapor_press_ChemAxon" class="ChemCalcs_unavailable chemaxon id_vapor_press" style="opacity: 1;"></td>
# <td id="id_vapor_press_EPI" class="ChemCalcs_available epi id_vapor_press" style="opacity: 0.75;"></td>
# <td id="id_vapor_press_TEST" class="ChemCalcs_available test id_vapor_press" style="opacity: 1;">899.8</td>
# <td id="id_vapor_press_SPARC" class="ChemCalcs_available sparc id_vapor_press" style="opacity: 0.75;"></td>
# <td id="id_vapor_press_MEASURED" class="ChemCalcs_available measured id_vapor_press" style="opacity: 1;">1820</td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_mol_diss" name="mol_diss" type="checkbox"> <span>Molecular Diffusivity (cm<sup>2</sup>/s)</span></th>
# <td id="id_mol_diss_ChemAxon" class="ChemCalcs_unavailable chemaxon id_mol_diss" style="opacity: 1;"></td>
# <td id="id_mol_diss_EPI" class="ChemCalcs_unavailable epi id_mol_diss" style="opacity: 1;"></td>
# <td id="id_mol_diss_TEST" class="ChemCalcs_unavailable test id_mol_diss" style="opacity: 1;"></td>
# <td id="id_mol_diss_SPARC" class="ChemCalcs_available sparc id_mol_diss" style="opacity: 1;"></td>
# <td id="id_mol_diss_MEASURED" class="ChemCalcs_unavailable measured id_mol_diss" style="opacity: 1;"></td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_ionization_con" name="ionization_con" type="checkbox"> <span>Ionization Constant</span></th>
# <td id="id_ionization_con_ChemAxon" class="ChemCalcs_available chemaxon id_ionization_con" style="opacity: 1;">2.954</td>
# <td id="id_ionization_con_EPI" class="ChemCalcs_unavailable epi id_ionization_con" style="opacity: 0.75;"></td>
# <td id="id_ionization_con_TEST" class="ChemCalcs_unavailable test id_ionization_con" style="opacity: 1;"></td>
# <td id="id_ionization_con_SPARC" class="ChemCalcs_available sparc id_ionization_con" style="opacity: 0.75;"></td>
# <td id="id_ionization_con_MEASURED" class="ChemCalcs_unavailable measured id_ionization_con" style="opacity: 1;"></td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_henrys_law_con" name="henrys_law_con" type="checkbox"> <span>Henry's Law Constant (atm-m<sup>3</sup>/mol)</span></th>
# <td id="id_henrys_law_con_ChemAxon" class="ChemCalcs_unavailable chemaxon id_henrys_law_con" style="opacity: 1;"></td>
# <td id="id_henrys_law_con_EPI" class="ChemCalcs_available epi id_henrys_law_con" style="opacity: 0.75;"></td>
# <td id="id_henrys_law_con_TEST" class="ChemCalcs_unavailable test id_henrys_law_con" style="opacity: 1;"></td>
# <td id="id_henrys_law_con_SPARC" class="ChemCalcs_available sparc id_henrys_law_con" style="opacity: 0.75;"></td>
# <td id="id_henrys_law_con_MEASURED" class="ChemCalcs_unavailable measured id_henrys_law_con" style="opacity: 1;"></td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_kow_no_ph" name="kow_no_ph" type="checkbox"> <span>Octanol/Water Partition Coefficient</span></th>
# <td id="id_kow_no_ph_ChemAxon" class="ChemCalcs_available chemaxon id_kow_no_ph" style="opacity: 1;">899.8</td>
# <td id="id_kow_no_ph_EPI" class="ChemCalcs_available epi id_kow_no_ph" style="opacity: 0.75;"></td>
# <td id="id_kow_no_ph_TEST" class="ChemCalcs_available test id_kow_no_ph" style="opacity: 1;">2.729</td>
# <td id="id_kow_no_ph_SPARC" class="ChemCalcs_available sparc id_kow_no_ph" style="opacity: 0.75;"></td>
# <td id="id_kow_no_ph_MEASURED" class="ChemCalcs_unavailable measured id_kow_no_ph" style="opacity: 1;"></td>
# </tr>



# <tr>
# <th class="chemprop"><input id="id_kow_wph" name="kow_wph" type="checkbox"> <span>Octanol/Water Partition Coefficient</span>



# <span>at pH:</span> <input id="id_kow_ph" name="kow_ph" size="1" type="text" value="7.4"></th>
# <td id="id_kow_ChemAxon" class="ChemCalcs_available chemaxon id_kow_ph" style="opacity: 1;">64.61</td>
# <td id="id_kow_EPI" class="ChemCalcs_unavailable epi id_kow_ph" style="opacity: 0.75;"></td>
# <td id="id_kow_TEST" class="ChemCalcs_unavailable test id_kow_ph" style="opacity: 1;"></td>
# <td id="id_kow_SPARC" class="ChemCalcs_available sparc id_kow_ph" style="opacity: 0.75;"></td>
# <td id="id_kow_MEASURED" class="ChemCalcs_unavailable measured id_kow_ph" style="opacity: 1;"></td>



# </tr><tr>
# <th class="chemprop"><input id="id_koc" name="koc" type="checkbox"> <span>Organic Carbon Partition Coefficient</span></th>
# <td id="id_koc_ChemAxon" class="ChemCalcs_unavailable chemaxon id_koc" style="opacity: 1;"></td>
# <td id="id_koc_EPI" class="ChemCalcs_available epi id_koc" style="opacity: 0.75;"></td>
# <td id="id_koc_TEST" class="ChemCalcs_unavailable test id_koc" style="opacity: 1;"></td>
# <td id="id_koc_SPARC" class="ChemCalcs_unavailable sparc id_koc" style="opacity: 0.75;"></td>
# <td id="id_koc_MEASURED" class="ChemCalcs_unavailable measured id_koc" style="opacity: 1;"></td>
# </tr>


# <tr>
# <th></th>
# <td class="ChemCalcs_available" style="opacity: 0.75;">Available</td>
# <td class="ChemCalcs_unavailable" style="opacity: 0.75;">Unavailable</td>
# </tr>
# </tbody></table>'''

# 	    html = html + render_to_string('export.html', {})
# 	    html = html + render_to_string('04uberoutput_end.html', {'model':model})
# 	    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
# 	    return HttpResponse(html)	

    outputmodule = importlib.import_module('.'+model+'_output', 'models.'+model)
    tablesmodule = importlib.import_module('.'+model+'_tables', 'models.'+model)
    # from REST import rest_funcs

    outputPageFunc = getattr(outputmodule, model+'OutputPage') # function name = 'model'OutputPage  (e.g. 'sipOutputPage')
    model_obj = outputPageFunc(request)

    if type(model_obj) is tuple:
        modelOutputHTML = model_obj[0]
        model_obj = model_obj[1]
    else:
        # logging.info(model_obj.__dict__)
        modelOutputHTML = tablesmodule.timestamp(model_obj)
        
        tables_output = tablesmodule.table_all(model_obj)
        
        if type(tables_output) is tuple:
            modelOutputHTML = modelOutputHTML + tables_output[0]
        elif type(tables_output) is str or type(tables_output) is unicode:
            modelOutputHTML = modelOutputHTML + tables_output
        else:
            modelOutputHTML = "table_all() Returned Wrong Type"

    # Render output page view
    html = render_to_string('01cts_uberheader.html', {'title': header+' Output'})
    html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'output'})
    html = html + linksLeft.linksLeft()
    html = html + render_to_string('04uberoutput_start.html', {
            'model_attributes': header+' Output'})

    html = html + modelOutputHTML
    html = html + render_to_string('export.html', {})
    html = html + render_to_string('04uberoutput_end.html', {'model':model})
    html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
    
    # Handle Trex, which is not objectified yet
    # if model != 'trex':
    #     rest_funcs.save_dic(html, model_obj.__dict__, model, "single")

    response = HttpResponse()
    response.write(html)
    return response

@require_POST
def outputPage(request, model='none', header=''):

    viewmodule = importlib.import_module('.views', 'models.'+model)

    header = viewmodule.header

    parametersmodule = importlib.import_module('.'+model+'_parameters', 'models.'+model)

    try:
        # Class name must be ModelInp, e.g. SipInp or TerrplantInp
        inputForm = getattr(parametersmodule, model.title() + 'Inp')
        
        form = inputForm(request.POST) # bind user inputs to form object

        # Form validation testing
        if form.is_valid():
            return outputPageView(request, model, header)

        else:

            inputmodule = importlib.import_module('.'+model+'_input', 'models.'+model)

            # Render input page view with POSTed values and show errors
            html = render_to_string('01cts_uberheader.html', {'title': header+' Inputs'})
            html = html + render_to_string('02cts_uberintroblock_wmodellinks.html', {'model':model,'page':'input'})
            html = html + linksLeft.linksLeft()

            inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
            html = html + inputPageFunc(request, model, header, formData=request.POST)  # formData contains the already POSTed form data

            html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
            
            response = HttpResponse()
            response.write(html)
            return response

        # end form validation testing

    except:
        
        logging.warning("E X C E P T")

        return outputPageView(request, model, header)
