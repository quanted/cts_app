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


    //disable all input fields unless checked:
    $('input').not('input[type="checkbox"], input[type="button"]').prop('disabled', true);

    enableTable($('input[type="checkbox"]'));

    $('input[type="checkbox"]').change(function() {

        enableTable(this);

    });



});


//Enables or disables table depending
//on its checkbox state
function enableTable(chkbox) {

    $(chkbox).each(function() {
        

        var isChecked = $(this).is(":checked");
        var chkName = $(this).attr("name");
        var tblName = $('input[name="' + chkName + '"]').closest('table').attr("name");

        if (isChecked) {
            $('table[name="' + tblName + '"] input[type="number"]').prop('disabled', false);
            $('table[name="' + tblName + '"] input[type="text"]').prop('disabled', false);
        }
        else {
            $('table[name="' + tblName + '"] input[type="number"]').prop('disabled', true);
            $('table[name="' + tblName + '"] input[type="text"]').prop('disabled', true);
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