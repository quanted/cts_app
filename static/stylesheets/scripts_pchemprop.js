$(document).ready(function() {

    uberNavTabs(
        ["Chemical", "ChemCalcs"],
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
    //     switch(isAllChecked_ChemCalcs) {
    //         case 1:
    //             isAllChecked_ChemCalcs = 0;
    //             $(".tab_ChemCalcs input").prop( "checked", true ); //checks all checkboxes within table
    //             // $(".col_header").prop("checked", false); //uncheck data source column headers
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

    //Initialize all checkboxes to be unchecked:
    // $("input:checkbox").prop('checked', false);

    // //Start with the cells containing classes ChemCalcs_available or ChemCalcs_unavailable;
    // //Make them slightly transparent, then darken a column that's selected.

    // $('.ChemCalcs_available').fadeTo(0, 0.75);  
    // $('.ChemCalcs_unavailable').fadeTo(0, 0.75);

    // //Highlight column of selected datasource:
    // $('#id_chemaxon_select').click(function() {
      
    //     if ($('#id_chemaxon_select').is(":checked"))
    //     {
    //         // $(this).closest('tr').switchClass('pchem_unchecked_col', 'pchem_checked_col');
    //         $('.chemaxon').fadeTo(0, 1);
    //     }
    //     else
    //     {
    //         // $(this).closest('tr').toggleClass('pchem_unchecked_col', 'pchem_unchecked_col'); 
    //         $('.chemaxon').fadeTo(0, 0.75);  
    //     }

    // });
    // $('#id_epi_select').click(function() {
      
    //     if ($('#id_epi_select').is(":checked"))
    //     {
    //         // $(this).closest('tr').switchClass('pchem_unchecked_col', 'pchem_checked_col');
    //         $('.epi').fadeTo(0, 1);
    //     }
    //     else
    //     {
    //         // $(this).closest('tr').toggleClass('pchem_unchecked_col', 'pchem_unchecked_col'); 
    //         $('.epi').fadeTo(0, 0.75);  
    //     }

    // });
    // $('#id_test_select').click(function() {
      
    //     if ($('#id_test_select').is(":checked"))
    //     {
    //         // $(this).closest('tr').switchClass('pchem_unchecked_col', 'pchem_checked_col');
    //         $('.test').fadeTo(0, 1);
    //     }
    //     else
    //     {
    //         // $(this).closest('tr').toggleClass('pchem_unchecked_col', 'pchem_unchecked_col'); 
    //         $('.test').fadeTo(0, 0.75);  
    //     }

    // });
    // $('#id_sparc_select').click(function() {
      
    //     if ($('#id_sparc_select').is(":checked"))
    //     {
    //         // $(this).closest('tr').switchClass('pchem_unchecked_col', 'pchem_checked_col');
    //         $('.sparc').fadeTo(0, 1);
    //     }
    //     else
    //     {
    //         // $(this).closest('tr').toggleClass('pchem_unchecked_col', 'pchem_unchecked_col'); 
    //         $('.sparc').fadeTo(0, 0.75);  
    //     }

    // });

});