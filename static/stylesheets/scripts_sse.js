//testing server-sent events
$(document).ready(function() {

	// var source = new EventSource("");
	var source = new EventSource("/jchem-cts/ws/test-sse");

	source.onmessage = function(e) {
		console.log(e.data);
	    // alert("sse worked!");
	};

});

