var pchempropsDefaults = ["chemaxon", "ion_con", "kow_no_ph", "kow_wph"]; //checkbox names

$(document).ready(function() {

    if ( typeof uberNavTabs == 'function' ) {
        uberNavTabs(
            ["Chemical", "ChemCalcs"],
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

    var isAllChecked_ChemCalcs = 1;

    var noOfInput_ChemCalcs = []
    $('#tab_ChemCalcs').find('input').push(noOfInput_ChemCalcs);
    noOfInput_ChemCalcs = noOfInput_ChemCalcs.length;
    var noOfInput_ChemCalcs = $(".tab_ChemCalcs input").length -1;

    var isChecked_ChemCalcs = [];
    $("#id_all").change(function() {
        switch(isAllChecked_ChemCalcs) {
            case 1:
                isAllChecked_ChemCalcs = 0;
                $(".chemprop input:checkbox").prop( "checked", true );
                console.log('Set checked');
                break;
            case 0:
                $(".chemprop input:checkbox").prop( "checked", false );
                isAllChecked_ChemCalcs = 1;
                console.log('Set unchecked');
                break;
            default:
                console.log('JavaScript Error');
        }
    });

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
    $('.submit.input_button').prop('disabled', true); //initialize submit as disabled


    $('input[type=checkbox]').change(function() {
        submitButtonLogic(); //tie submitLogic() to any checkbox changes
        pchempropTableLogic();
    });

    //Initialize all checkboxes to be unchecked:
    $("input:checkbox").prop('checked', false);

    //Start with the cells containing classes ChemCalcs_available or ChemCalcs_unavailable;
    //Make them slightly transparent, then darken a column that's selected.
    $('.ChemCalcs_available').fadeTo(0, 0.75);  
    $('.ChemCalcs_unavailable').fadeTo(0, 0.75);

    pchempropTableLogic();

});

function submitButtonLogic() {

    //Enable submit only when a calculator is 
    //checked AND an available property:

    //disable submit if no calculator is checked
    if ($('input[type=checkbox].col_header').is(':not(:checked)')) {
        $('.submit.input_button').prop('disabled', true);
    }

    //loop through calculators' checkboxes
    $('input[type=checkbox].col_header').each(function() {

        if ($(this).is(':checked')) {

            var calcName = $(this).attr('name');
            var availableProps = $('td.ChemCalcs_available.' + calcName);

            //enable submit if checked calculator has checked properties
            if ($(availableProps).parent().find('input[type=checkbox]').is(':checked')) {
                $('.submit.input_button').prop('disabled', false);
            }

        }

    });

}

function pchempropTableLogic() {
    //Highlight column of selected calculator:
    $('input.col_header').change(function() {
        var colClass = $(this).attr('name');
        if ($(this).is(':checked')) { $('td.' + colClass).fadeTo(0, 1); }
        else { $('td.' + colClass).fadeTo(0, 0.75); }
    });
}