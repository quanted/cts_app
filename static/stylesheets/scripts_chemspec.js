$(document).ready(function() {

    uberNavTabs(
        ["Chemical", "Speciation"],
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

    var isAllChecked_ChemCalcs = 1;

    var noOfInput_ChemCalcs = []
    $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    var isChecked_ChemCalcs = [];
    $("#id_all").click(function() {
        switch(isAllChecked_ChemCalcs) {
            case 1:
                isAllChecked_ChemCalcs = 0;
                $(".tab_ChemCalcs input").prop( "checked", true );
                console.log('Set checked');
                break;
            case 0:
                $(".tab_ChemCalcs input").prop( "checked", false );
                isAllChecked_ChemCalcs = 1;
                console.log('Set unchecked');
                break;
            default:
                console.log('JavaScript Error');
        }
    });

    //disable all input fields until checked:
    // $('input').not('input[type="checkbox"], input[type="button"]').prop('readonly', true);
    $('input').not('input[type="checkbox"], input[type="button"]').prop('readonly', true);

    enableTable($('input[type="checkbox"]'));

    $('input[type="checkbox"]').change(function() {
        enableTable(this);
    });

    $('table.tab_Speciation').hover(
        function() {
            //mouseenter
            $(this).removeClass('darken');
            $(this).find('input[type=checkbox]').addClass('brightBorders');
        },
        function() {
            //mouseleave
            var checked = $(this).find('input[type=checkbox]').is(':checked');
            if (!checked) {
                $(this).addClass('darken'); 
            }
            $(this).find('input[type=checkbox]').removeClass('brightBorders');
        }   
    );

});


//Enables or disables table depending
//on its checkbox state
function enableTable(chkbox) {

    $(chkbox).each(function() {

        var table = $(this).closest('table');

        if ($(this).is(":checked")) {
            table.find('input[type=number], input[type=text]').prop('readonly', false);
            table.removeClass('darken');
        }
        else {
            table.find('input[type=number], input[type=text]').prop('readonly', true);
            table.addClass('darken');
        }

        //Submit only enabled if a checkbox is selected:
        if ($('input[type="checkbox"]').is(":checked")) {
            $('input[type="submit"]').prop('disabled', false);
        }
        else {
            $('input[type="submit"]').prop('disabled', true);
        }

    });

}

// function enableTable(chkbox) {

//     $(chkbox).each(function() {
        

//         var isChecked = $(this).is(":checked");
//         var chkName = $(this).attr("name");
//         var tblName = $('input[name="' + chkName + '"]').closest('table').attr("name");

//         var table = $('input[name="' + chkName + '"]').closest('table');

//         if (isChecked) {
//             // $('table[name="' + tblName + '"] input[type="number"]').prop('readonly', false);
//             // $('table[name="' + tblName + '"] input[type="text"]').prop('readonly', false);
//             $(table).children('input').prop('readonly', false);
//             $('table[name="' + tblName + '"]').css({'opacity': 1.0});
//         }
//         else {
//             $('table[name="' + tblName + '"] input[type="number"]').prop('readonly', true);
//             $('table[name="' + tblName + '"] input[type="text"]').prop('readonly', true);
//             $('table[name="' + tblName + '"]').css({'opacity': 0.5});
//         }

//         //Submit only enabled if a checkbox is selected:
//         if ($('input[type="checkbox"]').is(":checked")) {
//             $('input[type="submit"]').prop('readonly', false);
//         }
//         else {
//             $('input[type="submit"]').prop('readonly', true);
//         }

//     });

// }