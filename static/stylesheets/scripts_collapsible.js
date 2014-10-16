$(document).ready(function () {
	$.fn.slideFadeToggle = function(speed, easing, callback) {
        return this.animate({opacity: 'toggle', height: 'toggle'}, speed, easing, callback);
    };
    var sect_all = $('.collapsible').map(function() {
    	return this.id;
    }).get().join();
	$('.collapsible').collapsible({
		speed: 'slow',
		defaultOpen: ""+sect_all+"", //original code 
        // defaultOpen: "chart1", //(np)
        //replace the standard slideDown with custom function
        animateOpen: function (elem, opts) {
            elem.next().slideFadeToggle(opts.speed);
        },
        //replace the standard slideUp with custom function
        animateClose: function (elem, opts) {
            elem.next().slideFadeToggle(opts.speed);
        }
	});


    //For Parent/Microspecies image tree 
    $('dt').click(function() {
        $(this).nextUntil('dt').slideToggle(700);
    });

});