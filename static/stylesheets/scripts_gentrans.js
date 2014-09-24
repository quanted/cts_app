$(document).ready(function() {

    uberNavTabs(
        ["Chemical", "ReactionPathSim", "ChemCalcs", "ReactionRateCalc"],
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

    // var isAllChecked_ChemCalcs = 1;

    // var noOfInput_ChemCalcs = []
    // $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    // noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    // var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    // var isChecked_ChemCalcs = [];
    // $("#id_all").click(function() {
    //     // for (var i=0;1<noOfInput_ChemCalcs;i++) {
    //     //     if ($(".tab_ChemCalcs input").prop( "checked" )) {

    //     //     }
    //     // }
    //     // if ($(".tab_ChemCalcs input").prop( "checked" )) {
    //     //     console.log($(".tab_ChemCalcs input").attr('id'));
    //     // }
    //     // switch(isAllChecked_ChemCalcs) {
    //     //     case 1:
    //     //         isAllChecked_ChemCalcs = 0;
    //     //         $(".tab_ChemCalcs input").prop( "checked", true );
    //     //         console.log('Set checked');
    //     //         break;
    //     //     case 0:
    //     //         $(".tab_ChemCalcs input").prop( "checked", false );
    //     //         isAllChecked_ChemCalcs = 1;
    //     //         console.log('Set unchecked');
    //     //         break;
    //     //     default:
    //     //         console.log('JavaScript Error');
    //     // }

    //     switch(isAllChecked_ChemCalcs) {
    //         case 1:
    //             isAllChecked_ChemCalcs = 0;
    //             $(".tab_ChemCalcs input").prop( "checked", true ); //checks all checkboxes within table
    //             $(".col_header").prop("checked", false); //uncheck data source column headers
    //             console.log('Set checked');
    //             break;
    //         case 0:
    //             $(".tab_ChemCalcs input").prop( "checked", false );
    //             isAllChecked_ChemCalcs = 1;
    //             console.log('Set unchecked');
    //             break;
    //         default:
    //             console.log('JavaScript Error');
    //     }
    // });


    // $('#id_reaction_systems').closest('tr').show();
    $('#cts_path_sime').show();
    $('#cts_react_sys').hide();
    $('#cts_respiration').hide();
    $('#cts_reaction_libs').hide();
    $('#cts_aerobic').hide();
    $('#cts_anaerobic').hide();

    $('#id_reaction_systems').val("0"); //Initialize with "Make a selection" value
    $('#id_respiration').val("0"); //Initialize with "Make a selection" value

    $("input[name='reaction_paths']").change(function() {
        if ($(this).val() == "0") {
            //If "Reaction System" is selected
            $('#cts_path_sim').show();
            $('#cts_react_sys').show();
            $('#cts_respiration').hide();
            $('#cts_aerobic').hide();
            $('#cts_anaerobic').hide();
            $('#cts_reaction_libs').hide();

            $('#id_respiration').val("0");
        }

        else if ($(this).val() == "1") {
            //If "OECD Guidelines" is checked..
            $('#cts_path_sim').show();
            $('#cts_react_sys').hide();
            $('#cts_respiration').show();
            $('#cts_aerobic').hide();
            $('#cts_anaerobic').hide();
            $('#cts_reaction_libs').hide();
            
        }
        else if ($(this).val() == "2") {
            //Show Reaction Library with "Reaction Library" checked
            $('#cts_path_sim').show();
            $('#cts_react_sys').hide();
            $('#cts_respiration').hide();
            $('#cts_aerobic').hide();
            $('#cts_anaerobic').hide();
            $('#cts_reaction_libs').show();

            //Set what's checkable in Reaction Libraries table
            $('#id_mamm_metabolism').prop('checked', true);
            $('#id_abiotic_hydrolysis').prop('disabled', true);
            $('#id_aerobic_biodegrad').prop('disabled', true);
            $('#id_photolysis').prop('disabled', true);
            $('#id_abiotic_reduction').prop('disabled', true);
            $('#id_anaerobic_biodegrad').prop('disabled', true);
            $('#id_mamm_metabolism').prop('disabled', true);
        }
    });

    $("input[name='reaction_system']").change(function() {
        if ($(this).val() == "0") {
            //If "Environmental" is selected..
            $('#cts_respiration').show();
            $('#cts_aerobic').hide();
            $('#cts_anaerobic').hide();
            $('#cts_reaction_libs').hide();
            
        }
        else if ($(this).val() == "1") {
            //Show Reaction Library with "Mammalian" selected

            $('#cts_respiration').hide();
            $('#cts_aerobic').hide();
            $('#cts_anaerobic').hide();
            $('#cts_reaction_libs').show();

            //Set what's checkable in Reaction Libraries table
            $('#id_mamm_metabolism').prop('checked', true);
            $('#id_abiotic_hydrolysis').prop('disabled', true);
            $('#id_aerobic_biodegrad').prop('disabled', true);
            $('#id_photolysis').prop('disabled', true);
            $('#id_abiotic_reduction').prop('disabled', true);
            $('#id_anaerobic_biodegrad').prop('disabled', true);
            $('#id_mamm_metabolism').prop('disabled', true);
        }
    });

    $("input[name='respiration']").change(function() {
        if ($(this).val() == "0") {
            //Display aerobic table...
            $('#cts_respiration').show();
            $('#cts_aerobic').show();
            $('#cts_anaerobic').hide();
            $('#cts_reaction_libs').show();

            //Set Reaction Libraries table...
            $('#id_mamm_metabolism').prop('checked', false);
            $('#id_abiotic_hydrolysis').prop('disabled', false);
            $('#id_aerobic_biodegrad').prop('disabled', false);
            $('#id_photolysis').prop('disabled', false);
            $('#id_abiotic_reduction').prop('disabled', false);
            $('#id_anaerobic_biodegrad').prop('disabled', true);
            $('#id_mamm_metabolism').prop('disabled', true);
        }
        else if ($(this).val() == "1") {
            //Display anaerobic table...
            $('#cts_respiration').show();
            $('#cts_aerobic').hide();
            $('#cts_anaerobic').show();
            $('#cts_reaction_libs').show();

            //Set Reaction Libraries table...
            $('#id_mamm_metabolism').prop('checked', false);
            $('#id_abiotic_hydrolysis').prop('disabled', false);
            $('#id_aerobic_biodegrad').prop('disabled', true);
            $('#id_photolysis').prop('disabled', false);
            $('#id_abiotic_reduction').prop('disabled', false);
            $('#id_anaerobic_biodegrad').prop('disabled', false);
            $('#id_mamm_metabolism').prop('disabled', true);
        }
    });

});