//TODO: Rework this segment of code. It can easily be
//halfed, maybe more.
$(document).ready(function() {

    //Initialize all checkboxes to be unchecked:
    $("input:checkbox").prop('checked', false);

    //Start with the cells containing classes ChemCalcs_available or ChemCalcs_unavailable;
    //Make them slightly transparent, then darken a column that's selected.
    $('.ChemCalcs_available').fadeTo(0, 0.75);  
    $('.ChemCalcs_unavailable').fadeTo(0, 0.75);

    $('#id_sparc_select').prop('disabled', true); // disable sparc until web services are working

    pchempropTableLogic();

    var isAllChecked_ChemCalcs = 1;
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

});

function pchempropTableLogic() {
    //Highlight column of selected calculator:
    $('input.col_header').change(function() {
        var colClass = $(this).attr('name');
        if ($(this).is(':checked')) { $('td.' + colClass).fadeTo(0, 1); }
        else { $('td.' + colClass).fadeTo(0, 0.75); }
    });
}
