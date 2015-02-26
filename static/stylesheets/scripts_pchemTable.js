//TODO: Rework this segment of code. It can easily be
//halfed, maybe more.
$(document).ready(function() {

    //Initialize all checkboxes to be unchecked:
    $("input:checkbox").prop('checked', false);

    //Start with the cells containing classes ChemCalcs_available or ChemCalcs_unavailable;
    //Make them slightly transparent, then darken a column that's selected.
    $('.ChemCalcs_available').fadeTo(0, 0.75);  
    $('.ChemCalcs_unavailable').fadeTo(0, 0.75);

    pchempropTableLogic();

});

function pchempropTableLogic() {
    //Highlight column of selected calculator:
    $('input.col_header').change(function() {
        var colClass = $(this).attr('name');
        if ($(this).is(':checked')) { $('td.' + colClass).fadeTo(0, 1); }
        else { $('td.' + colClass).fadeTo(0, 0.75); }
    });
}
