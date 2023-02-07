//+++++++++++++++++++++++++++++++++++++++++
//Selection logic for the Reaction Pathway
//Simulator in the gentrans workflow
//
//TODO: refactor this atrocity!!!!!
//+++++++++++++++++++++++++++++++++++++++++

$(document).ready(function() {

    var disablePhotolysis = false;
    var disableBiotrans = false;
    var disableEnvipath = false;
    var disableQsar = false;
    var disablePfas = false;

    // TODO: Flags per feature conditionals instead of env name conditions
    if (
        envName == "gdit_aws_stg" || 
        envName == "cgi_azure_docker_dev" || 
        envName == "saic_aws_docker_prod" ||
        envName == "epa_aws_stg" ||
        envName == "epa_aws_prd"
    ) {
        // disablePhotolysis = true;
        // disableBiotrans = true;
        // disableEnvipath = true;
        disableQsar = true;
    }

    var gentrans_tables = '#oecd_selection, #ftt_selection, #health_selection, ' +
                            '#cts_reaction_sys, #respiration_tbl, #mammalian_choices_tbl'; // tables to hide/show

    var unaviable_options = 'select[name=pop_limit], ' +
        '#id_aerobic_biodegrad, #id_anaerobic_biodegrad';

    if (typeof uberNavTabs == 'function') {
        uberNavTabs(
            ["Chemical", "ReactionPathSim"],
            {   "isSubTabs":true,
            	"Chemical": [".tab_chemicalButtons"] }
        );
    }

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    });

    $('input[type=radio], input[type=checkbox]').prop('checked', false); // clear data

    $(gentrans_tables).hide();

    $(unaviable_options).prop('disabled', true); // these options are currently not available

    // disable checkboxes and submit button
    // $('#cts_reaction_libs input[type="checkbox"], input.submit').prop('disabled', true);
    $('#cts_reaction_libs input[type="checkbox"], \
        #cts_class_specific_reaction_libs input[type="checkbox"], \
        #id_biotrans_libs').prop('disabled', true);

    brightenBorder($('#cts_reaction_paths')); // brighten first table for user input


    if ($('table#cts_biotrans_libs').length > 0) {
        $('input.submit').addClass('brightBorders');
    }


    $("input[name='reaction_paths']").change(function() {

        $(gentrans_tables).hide();

        if ($(this).val() == "0") {
            // Reaction System Guidelines
            $('#cts_reaction_sys').show();
            clearReactionLib();
            brightenBorder($('#cts_reaction_sys'));
        }

        else if ($(this).val() == "1") {
            // OCSPP Guidelines
            $('#oecd_selection').show();
            clearReactionLib();
            brightenBorder($('#oecd_selection'));
        }

        else if ($(this).val() == "2") {
            // User selected (advanced)
            $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': false, 'disabled':false}).trigger('change');
            $('#id_mamm_metabolism').prop({'checked': false, 'disabled':false}).trigger('change');
            if (!disablePhotolysis) {
                $('#id_photolysis_unranked').prop({'checked': false, 'disabled':false}).trigger('change');
                $('#id_photolysis_ranked').prop({'checked': false, 'disabled':false}).trigger('change');
            }
            if (!disableBiotrans) {
                $('#id_biotrans_metabolism').prop({'checked': false, 'disabled':false}).trigger('change');
                $('#id_biotrans_libs').prop({'disabled':false}).trigger('change');   
            }
            if (!disableEnvipath) {
                $('#id_envipath_metabolism').prop({'checked': false, 'disabled':false}).trigger('change');
            }
            if (!disablePfas) {
                $('#id_pfas_metabolism').prop({'checked': false, 'disabled':false}).trigger('change');
                $('#id_pfas_environmental').prop({'checked': false, 'disabled':false}).trigger('change');   
            }
            brightenBorder($('#cts_reaction_libs, #cts_class_specific_reaction_libs'));
        }

        clearHiddenInputs();

    });

    $("input[name='reaction_system']").change(function() {

        $(gentrans_tables).hide();

        clearReactionLib();

        if ($(this).val() == "0") {
            //If "Environmental" is selected..
            $('#cts_reaction_sys, #respiration_tbl').show();
            brightenBorder($('#respiration_tbl'));
        }

        else if ($(this).val() == "1") {
            //Shows "Select a mammalian library" table
            $('#cts_reaction_sys, #mammalian_choices_tbl').show();
            // Sets chemaxon metabolizer as default
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        clearHiddenInputs();

    });

    $('select[name="respiration"]').change(function() {

        $(gentrans_tables).hide();
        $('#cts_reaction_sys, #respiration_tbl').show();

        clearReactionLib();

        if ($(this).val() == "0") {
            // clearReactionLib();
            brightenBorder($(this).closest('table'));
        }

        else if ($(this).val() == "1") {

            // Sets reaction library options for aerobic (abiotic) option
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_photolysis_ranked').prop({'checked': true, 'disabled':false}).trigger('change');
            // $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true}).trigger('change');
            // $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        else if ($(this).val() == "2") {
            // Sets reaction library options for aerobic (microbial) option
            $('#id_envipath_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            // $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            // $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        else if ($(this).val() == "3") {
            // Sets reaction library options for anaerobic option
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            // $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

    });

    $('select[name="mammalian_choices"]').change(function() {

        // $(gentrans_tables).hide();
        // $('#cts_reaction_sys, #mammalian_choices_tbl').show();
        $('#mammalian_choices_tbl').show();

        clearReactionLib();

        if ($(this).val() == "0") {
            // Chemaxon Metabolizer selected
            // brightenBorder($(this).closest('table'));
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        else if ($(this).val() == "1") {
            // Biotransformer selected
            $('#id_biotrans_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_biotrans_libs').prop({'disabled':false}).trigger('change');
            $('#id_biotrans_libs').val("hgut");
            brightenBorder($('#cts_reaction_libs'));
        }

    });

    $("input[name='oecd_selection']").change(function() {

        //FTT content columns
        $('#labAbioTrans_picks').hide();
        $('#transWaterSoil_picks').hide();
        $('#transChemSpec_picks').hide();

        $(gentrans_tables).hide();

        clearReactionLib();

        if ($(this).val() == "0") {
            // FTT is selected
            $('#oecd_selection').show();
            $('#ftt_selection').show();
            // clearReactionLib();
            brightenBorder($('#ftt_selection'));
        }
        else if ($(this).val() == "1") {
            // "Metabolism and Pharmacokinetics" is selected
            $('#oecd_selection, #mammalian_choices_tbl').show();
            //Show Reaction Library with "Mammalian" selected
            // Sets chemaxon metabolizer as default
            $('#id_mamm_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

        // clearHiddenInputs();

    });

    $('select[name="ftt_selection"]').change(function() {

        var value = $(this).val();

        $(gentrans_tables).hide();

        $('#oecd_selection').show();
        $('#ftt_selection').show();

        clearReactionLib();

        if ($(this).val() == "0") {
            // Shows 'Make a selection'
            brightenBorder($(this).closest('table'));
        }
        else if ($(this).val() == "1") {
            // Hydrolysis selected
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }
        else if ($(this).val() == "2") {
            // Direct Photolysis selected
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_photolysis_ranked').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }
        else if ($(this).val() == "3") {
            // Aerobic Transformation selected
            $('#id_envipath_metabolism').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }
        else if ($(this).val() == "4") {
            // Anaerobic Transformation selected
            $('#id_abiotic_hydrolysis').prop({'checked': true, 'disabled':false}).trigger('change');
            $('#id_abiotic_reduction').prop({'checked': true, 'disabled':false}).trigger('change');
            brightenBorder($('#cts_reaction_libs'));
        }

    });

    // Enable submit only if a reaction library is selected
    $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').on("change", function() {

        let checkedItems = $('#cts_reaction_libs input:checkbox:checked, #cts_class_specific_reaction_libs input:checkbox:checked');

        let mamm_meta_checked = $('#id_mamm_metabolism:checked').length > 0;
        let areduct_checked = $('#id_abiotic_reduction:checked').length > 0;
        let ahydro_checked = $('#id_abiotic_hydrolysis:checked').length > 0;
        let photolysis_unranked_checked = $('#id_photolysis_unranked:checked').length > 0;
        let photolysis_ranked_checked = $('#id_photolysis_ranked:checked').length > 0;
        let biotrans_checked = $('#id_biotrans_metabolism:checked').length > 0;
        let envipath_checked = $('#id_envipath_metabolism:checked').length > 0;
        let pfas_environmental_checked = $('#id_pfas_environmental:checked').length > 0;
        let pfas_metabolism_checked = $('#id_pfas_metabolism:checked').length > 0;

        let tree_type_value = $('#id_tree_type').find(':selected').val();

        if (mamm_meta_checked && checkedItems.length != 1) {
            alert("Mammalian metabolism reaction library cannot run with additional reaction libraries");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false);
        }
        else if (biotrans_checked && checkedItems.length != 1) {
            alert("Biotransformer reaction library cannot run with additional reaction libraries");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false);
        }
        else if (envipath_checked && checkedItems.length != 1) {
            alert("Envipath reaction library cannot run with additional reaction libraries");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false); 
        }
        else if (photolysis_unranked_checked && checkedItems.length != 1) {
            alert("Unranked direct photolysis reaction library cannot run with additional reaction libraries");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false);
        }
        else if (pfas_environmental_checked && checkedItems.length != 1) {
            alert("PFAS environmental reaction library cannot run with additional reaction libraries");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false);   
        }
        else if (pfas_metabolism_checked && checkedItems.length != 1) {
            alert("PFAS metabolism reaction library cannot run with additional reaction libraries");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false);
        }
        else if (photolysis_ranked_checked && (photolysis_unranked_checked || areduct_checked)) {
            alert("Ranked direct photolysis reaction library can only be combined with abiotic hydrolysis library");
            $('#cts_reaction_libs input:checkbox, #cts_class_specific_reaction_libs input:checkbox').prop('checked', false);
        }

        if ($('#cts_reaction_libs input:checkbox:checked, #cts_class_specific_reaction_libs input:checkbox:checked').length > 0) {
            $('input.submit').addClass('brightBorders');
        }
        else {
            $('input.submit').removeClass('brightBorders');
        }

        if (photolysis_unranked_checked || photolysis_ranked_checked || biotrans_checked || envipath_checked) {
            // limits generation to 2 for photolysis library:
            $('select#id_gen_limit').children('option[value="3"], option[value="4"]').attr('disabled', true);
        }
        else {
            $('select#id_gen_limit').children('option[value="3"], option[value="4"]').attr('disabled', false);
        }

        if (ahydro_checked === true && disableQsar === false && tree_type_value === 'full_tree') {
            // Enables half-life checkbox for abiotiotic hydrolysis
            $('input#id_include_rates').attr('disabled', false);
        }
        else {
            $('input#id_include_rates').attr('disabled', true);
        }

    });

    $('#id_tree_type').on('change', function() {
        let tree_type_value = $('#id_tree_type').find(':selected').val();
        let ahydro_checked = $('#id_abiotic_hydrolysis:checked').length > 0;
        if (ahydro_checked === true && disableQsar === false && tree_type_value === 'full_tree') {
            // Enables half-life checkbox for abiotiotic hydrolysis
            $('input#id_include_rates').attr('disabled', false);
        }
        else {
            $('input#id_include_rates').attr('disabled', true);
        }
    });

});


function brightenBorder(element) {
    // remove border from previous, add to current
    $('table').removeClass('brightBorders'); // remove all 
    $(element).addClass('brightBorders'); // add to specified element
}


function clearReactionLib() {
    $('#id_abiotic_hydrolysis').prop({'checked': false, 'disabled':true});  //.trigger('change');
    $('#id_abiotic_reduction').prop({'checked': false, 'disabled':true});  //.trigger('change');
    $('#id_mamm_metabolism').prop({'checked': false, 'disabled':true});  //.trigger('change');
    $('#id_photolysis_unranked').prop({'checked': false, 'disabled':true});  //.trigger('change');
    $('#id_photolysis_ranked').prop({'checked': false, 'disabled':true});
    $('#id_biotrans_metabolism').prop({'checked': false, 'disabled':true});
    $('#id_biotrans_libs').prop({'disabled':true});
    $('#id_envipath_metabolism').prop({'checked': false, 'disabled':true});
    $('input#id_include_rates').attr({'checked': false, 'disabled': true});
    $('#id_biotrans_libs').val("cyp450");
    $('#id_pfas_metabolism').attr({'checked': false, 'disabled': true});
    $('#id_pfas_environmental').attr({'checked': false, 'disabled': true});
}


function clearHiddenInputs() {
    // clear all radios and selects that are hidden:
    var hidden_inputs = $('div.tab_ReactionPathSim :input:hidden');
    for (index in hidden_inputs) {
        if (hidden_inputs.hasOwnProperty(index)) {
            var input = hidden_inputs[index];
            if (input.type == "radio") {
                $(input).prop('checked', false);
            }
            else if (input.type == "select-one") {
                $(input).val("0"); 
            }
        }
    }
}