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

    //Highlight column of selected datasource:
    $('#id_chemaxon_select').change(function() {
      
        if ($('#id_chemaxon_select').is(":checked"))
        {
            $('.chemaxon').fadeTo(0, 1);
        }
        else
        {
            $('.chemaxon').fadeTo(0, 0.75);  
        }

    });
    $('#id_epi_select').change(function() {
      
        if ($('#id_epi_select').is(":checked"))
        {
            $('.epi').fadeTo(0, 1);
        }
        else
        {
            $('.epi').fadeTo(0, 0.75);  
        }

    });
    $('#id_test_select').change(function() {
      
        if ($('#id_test_select').is(":checked"))
        {
            $('.test').fadeTo(0, 1);
        }
        else
        {
            $('.test').fadeTo(0, 0.75);  
        }

    });
    $('#id_sparc_select').change(function() {
      
        if ($('#id_sparc_select').is(":checked"))
        {
            $('.sparc').fadeTo(0, 1);
        }
        else
        {
            $('.sparc').fadeTo(0, 0.75);  
        }

    });
}
