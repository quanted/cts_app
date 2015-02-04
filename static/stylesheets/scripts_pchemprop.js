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

    $()

});


//Enables submit button when at least one calculator and
//property (that's available) is checked. 
// function submitGateKeeper() {

// }