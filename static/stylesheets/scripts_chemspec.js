var chemspecDefaults = {
    "pKa_decimals": 2,
    "pKa_pH_lower": 0,
    "pKa_pH_upper": 14,
    "pKa_pH_increment": 0.2,
    "pH_microspecies": 7.0,
    "isoelectricPoint_pH_increment": 0.5,
    "tautomer_maxNoOfStructures": 100,
    "tautomer_pH": 7.0,
    "stereoisomers_maxNoOfStructures": 100
};

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

    $('#resetbutton').parent('li').show(); // only workflow with defaults button

    //var isAllChecked_ChemCalcs = 1;

    //var noOfInput_ChemCalcs = [];
    //$('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    //noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    //var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    //var isChecked_ChemCalcs = [];
    //$("#id_all").click(function() {
    //    switch(isAllChecked_ChemCalcs) {
    //        case 1:
    //            isAllChecked_ChemCalcs = 0;
    //            $(".tab_ChemCalcs input").prop( "checked", true );
    //            console.log('Set checked');
    //            break;
    //        case 0:
    //            $(".tab_ChemCalcs input").prop( "checked", false );
    //            isAllChecked_ChemCalcs = 1;
    //            console.log('Set unchecked');
    //            break;
    //        default:
    //            console.log('JavaScript Error');
    //    }
    //});

    //default button
    $('#resetbutton').click(function(){
        //load default values to fields 
        for (key in chemspecDefaults) {
            if (chemspecDefaults.hasOwnProperty(key)) {
                $('input[name=' + key + ']').val(chemspecDefaults[key]);
            }
        }
        //check first table (calculate ionization constants parameters)
        var defaultChkbox = $('input[name=pka_chkbox]');
        $(defaultChkbox).prop('checked', true);
        enableTable(defaultChkbox);
    });

    //disable all input fields until checked:
    $('input').not('input[type="checkbox"], input[type="button"]').prop('readonly', true);

    enableTable($('input[type="checkbox"]'));

    $('input[type="checkbox"]').change(function() {
        enableTable(this);
    });

    //mouseover speciation table - highlight its textbox:
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

    // todo: fix this so that the user can still click the checkbox itself
    //$('table.tab_Speciation').click(function() {
    //    // check the table's checkbox if table is clicked:
    //    var checkBox = $(this).find('input[type=checkbox]');
    //    if ($(checkBox).is(':checked')) {
    //        $(checkBox).prop('checked', false).trigger('change');
    //    }
    //    else {
    //        $(checkBox).prop('checked', true).trigger('change');
    //    }
    //
    //});

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
            $('input[type="submit"]').prop('disabled', false).addClass('brightBorders');
        }
        else {
            $('input[type="submit"]').prop('disabled', true).removeClass('brightBorders');
        }

    });

}