//+++++++++++++++++++++++++++++++++++++++++
//Selection logic for the Reaction Pathway
//Simulator in the gentrans workflow
//
//TODO: refactor this atrocity
//+++++++++++++++++++++++++++++++++++++++++

$(document).ready(function() {

    uberNavTabs(
        ["Chemical", "ReactionPathSim"],
        {   "isSubTabs":true,
        	"Chemical": [".tab_chemicalButtons"] }
    );

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    	// $('#chemEditLookup').hide();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    	// $('#chemEditDraw').hide();
    });

    // Clear data:
    $('input[type=checkbox]').prop('checked', false);
    $('input[type=radio]').prop('checked', false);

    // Main tables
    $('#cts_reaction_paths').show();
    $('#oecd_selection').hide();
    $('#ftt_selection').hide();
    $('#health_selection').hide();
    $('#cts_reaction_sys').hide();
    $('#respiration_tbl').hide();
    $('#cts_reaction_libs').hide();
    $('#cts_reaction_options').hide();

    //Respiration table contents
    $('#aerobic_picks').hide();
    $('#anaerobic_picks').hide();

    //Options for these options are currently not available
    $('select[name="ftt_selection"] option[value="2"]').prop('disabled', true);
    $('select[name="ftt_selection"] option[value="3"]').prop('disabled', true);

    $('select[name="pop_limit"]').prop('disabled', true); //disable pop limit until it actually does something

    $('#id_aerobic_biodegrad').prop('disabled', true);
    $('#id_anaerobic_biodegrad').prop('disabled', true);

    //Disable checkboxes (only enable for "Reaction Pathway" selection)
    $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);
    $('input.submit').prop('disabled', true); //initialize submit button to be disabled

    $("input[name='reaction_paths']").change(function() {
        if ($(this).val() == "0") {
            //If "Reaction System" is selected
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
            $('#cts_reaction_options').hide();
        }

        else if ($(this).val() == "1") {
            //If "OECD Guidelines" is checked..
            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
            $('#cts_reaction_options').hide();
        }

        else if ($(this).val() == "2") {
            //Show Reaction Library with "Reaction Library" checked
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').show();
            $('#cts_reaction_options').show();

            //Set Reaction Libraries table...
            // $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', false);

            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':false}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':false}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':false}).trigger('change');
        }
    });

    $("input[name='reaction_system']").change(function() {

        // $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

        if ($(this).val() == "0") {
            //If "Environmental" is selected..
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').show();
            $('#cts_reaction_libs').hide();
            $('#cts_reaction_options').hide();
        }
        else if ($(this).val() == "1") {
            //Show Reaction Library with "Mammalian" selected
            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').show();
            $('#cts_reaction_options').show();

            // $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

            //Set what's checkable in Reaction Libraries table
            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
        }
    });

    // $("#id_respiration").change(function() {
    $('select[name="respiration"]').change(function() {

        // $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

        //Main tables
        $('#cts_reaction_paths').show();
        $('#oecd_selection').hide();
        $('#ftt_selection').hide();
        $('#health_selection').hide();
        $('#cts_reaction_sys').show();
        $('#respiration_tbl').show();
        $('#cts_reaction_libs').show();
        $('#cts_reaction_options').show();

        if ($(this).val() == "0") {

            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').show();
            $('#cts_reaction_libs').hide();
            $('#cts_reaction_options').hide();

        }

        else if ($(this).val() == "1") {
            //Display aerobic column...
            // $('#aerobic_picks').show();
            // $('#anaerobic_picks').hide();

            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').show();
            $('#cts_reaction_libs').show();
            $('#cts_reaction_options').show();

            //Set Reaction Libraries ...
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');

        }
        else if ($(this).val() == "2") {
            //Display anaerobic column...
            // $('#aerobic_picks').hide();
            // $('#anaerobic_picks').show();

            $('#cts_reaction_paths').show();
            $('#oecd_selection').hide();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').show();
            $('#respiration_tbl').show();
            $('#cts_reaction_libs').show();
            $('#cts_reaction_options').show();

            //Set Reaction Libraries table...
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
        }
    });

    $("input[name='oecd_selection']").change(function() {

        // $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

        //FTT content columns
        $('#labAbioTrans_picks').hide();
        $('#transWaterSoil_picks').hide();
        $('#transChemSpec_picks').hide();

        if ($(this).val() == "0") {
            //If FTT is selected

            //Main tables
            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').show();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
            $('#cts_reaction_options').hide();
        }
        else if ($(this).val() == "1") {
            //If "Health Effects" is selected

            //Main tables
            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').hide();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').show();
            $('#cts_reaction_options').show();

            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');

        }
    });

    // $("#id_ftt_selection").change(function() {
    $('select[name="ftt_selection"]').change(function() {

        // $('#cts_reaction_libs input[type="checkbox"]').prop('disabled', true);

        var value = $(this).val();
        //Main tables
        $('#cts_reaction_paths').show();
        $('#oecd_selection').show();
        $('#ftt_selection').show();
        $('#health_selection').hide();
        $('#cts_reaction_sys').hide();
        $('#respiration_tbl').hide();
        $('#cts_reaction_libs').show();
        $('#cts_reaction_options').show();

        if ($(this).val() == "0") {

            $('#cts_reaction_paths').show();
            $('#oecd_selection').show();
            $('#ftt_selection').show();
            $('#health_selection').hide();
            $('#cts_reaction_sys').hide();
            $('#respiration_tbl').hide();
            $('#cts_reaction_libs').hide();
            $('#cts_reaction_options').hide();
            
        }

        if ($(this).val() == "1") {
            //If  Laboratory Abiotic Transformation Guidelines is selected

            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            
        }
        else if ($(this).val() == "2") {
            //If Transformation in Water and Soil Test Guidelines is selected

            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');

        }
        else if ($(this).val() == "3") {
            //If Transformation Chemcial-Specific Test Guidelines is selected

            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_aerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_photolysis').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_anaerobic_biodegrad').prop({'checked': false, 'disabled':true}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');

        }
    });

    // Enable submit only if a reaction library is selected
    $('#cts_reaction_libs input:checkbox').on("change", function() {
        if ($('#cts_reaction_libs input:checkbox:checked').length > 0) {
            $('input.submit').prop('disabled', false);
        }
        else {
            $('input.submit').prop('disabled', true);
        }
    });

});