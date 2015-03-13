var pchempropsDefaults = ["chemaxon", "ion_con", "kow_no_ph", "kow_wph"]; //checkbox names

$(document).ready(function() {

    uberNavTabs(
        ["Chemical", "ChemCalcs"],
        {   "isSubTabs":true,
        	"Chemical": [".tab_chemicalButtons"] }
    );

    $('#chemEditDraw_button').click(function() {
    	$('#chemEditDraw').show();
    });

    $('#chemEditLookup_button').click(function() {
    	$('#chemEditLookup').show();
    });

    // var isAllChecked_ChemCalcs = 1;

    //default button
    $('#resetbutton').click(function(){
        //check chemaxon and its avaiable properties
        for (i in pchempropsDefaults) {
            var chkbox = $('input[type=checkbox][name=' + pchempropsDefaults[i] + ']');
            $(chkbox).prop('checked', true);
        }
        $('.chemaxon').fadeTo(0, 1); //highlight chemaxon column
        $('#id_kow_ph').val(7.4);
    });

    //submit button logic:
    $('input[type=submit]').prop('disabled', true); //initialize submit as disabled


    $('input[type=checkbox]').change(function() {
        submitButtonLogic(); //tie submitLogic() to any checkbox changes
    });

});


function submitButtonLogic() {

    //Enable submit only when a calculator is 
    //checked AND an available property:

    var calcCheckboxes = $('input[type=checkbox].col_header');

    //loop through calculators' checkboxes
    calcCheckboxes.each(function() {
        if (this.checked) {
            var availableProps = $('td.ChemCalcs_available.' + this.name);
            //enable submit if checked calculator has checked properties
            if ($(availableProps).parent().find('input[type=checkbox]').is(':checked')) {
                $('input[type=submit]').prop('disabled', false);
            }
            else {
                $('input[type=submit]').prop('disabled', true);
            }
        }
    });

    var selectAllChecked = $('#id_all').is(':checked');
    var aCalcChecked = $(calcCheckboxes).is(':checked');
    var aPropChecked = $('th.chemprop input:checkbox').is(':checked');

    //if all is selected and any calculator, enable submit:
    if (selectAllChecked && aCalcChecked) {
        $('input[type=submit]').prop('disabled', false);
    }


    //MAYBE JUST GO BACK TO HAVING THE SELECT_ALL LOGIC IN THIS FILE...THIS IS
    //BECOMING AN ORDEAL GETTING IT TO WORK THIS WAY
    
    // if (!aPropChecked || !selectAllChecked) {
    //     $('input[type=submit]').prop('disabled', true);
    // }

}