var doneDiv = document.getElementById("popup");

$(document).ready(function () {

	function parseOutput(file_type) {
		
        var elements, jq_html, imgData_json, n_plot;
        var workflow = getWorkflow(); // get current workflow name
        var options = { x_offset : 30, y_offset : 30 }; // jqplotToImage options
        var imgData = []; // jqplot images
        var jsonData = ""; // json data string (originally intended for metabolites)

        elements = collectDOM(workflow); // get relevant dom objects

        if (file_type == "pdf" || file_type == "html") {
       		if (workflow == "chemspec") {
	            try {
	                imgData.push($('#microspecies-distribution').jqplotToImageStr(options));
	                imgData.push($('#isoelectric-point').jqplotToImageStr(options));
	            }
	            catch(e) { console.log(e); }
	        }
	        else if (workflow == "gentrans") {
	            var canvasNodes = getSpaceTree().graph.nodes;
	            var nodeArray = [];
	            for (var node in canvasNodes) {
	                if (canvasNodes.hasOwnProperty(node)) {
	                    var nodeItem = {
	                        'image': canvasNodes[node]['name'],
	                        'data': canvasNodes[node]['data']
	                    };
	                    nodeArray.push(nodeItem);
	                }
	            }
	            jsonData = JSON.stringify(nodeArray);  // spacetree data (cts_gentrans_tree.html)
	        }
			jq_html = $('<div />').append($(elements).clone()).html();
			var n_plot_1 = $('#microspecies-distribution').size();
			var n_plot_2 = $('#isoelectric-point').size();
			n_plot = n_plot_1 + n_plot_2;
			imgData_json = JSON.stringify(imgData, null, '\t');
        }
        else if (file_type == "csv") {
        	// send json object, no need for
        	// html elements like pdf/html uses
        	var content = buildCSV(workflow);
        	json_obj = { "headers": content[0], "data": content[1], "structure_info": content[2] };
        	jsonData = JSON.stringify(json_obj);
        }
        else { return; }

        appendToRequestTable(jq_html, n_plot, imgData_json, jsonData); // append elements to request table

	}

	$('#pdfExport').click(function () {
		parseOutput('pdf');
		$('form').attr({'action': 'pdf', 'method': 'POST'}).submit();
	});

	$('#htmlExport').click(function () {
		parseOutput('html');
		$('form').attr({'action': 'html', 'method': 'POST'}).submit();
	});

	$('#csvExport').click(function () {
        parseOutput('csv');
       	$('form').attr({'action': 'csv', 'method': 'POST'}).submit(); 
	});


	$('#fadeExport_pdf').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});
	
	$('#fadeExport_html').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});

	$('#fadeExport_csv').append('<span class="hover"></span>').each(function () {
		var $span = $('> span.hover', this).css('opacity', 0);
		$(this).hover(function () {
			$span.stop().fadeTo(500, 1);
		}, function () {
			$span.stop().fadeTo(500, 0);
		});
	});

});


function appendToRequestTable(jq_html, n_plot, imgData_json, jsonData) {
	
	var test = $('table.getpdf');

	$('table.getpdf').html("");
	
	$('<tr style="display:none"><td><input type="hidden" name="pdf_t"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(jq_html);

	$('<tr style="display:none"><td><input type="hidden" name="pdf_nop"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(n_plot);

	$('<tr style="display:none"><td><input type="hidden" name="pdf_p"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(imgData_json);

    $('<tr style="display:none"><td><input type="hidden" name="pdf_json"></td></tr>')
		.appendTo('.getpdf')
		.find('input')
		.val(jsonData); 
}


function collectDOM(workflow) {
	switch(workflow) {
		case "chemspec":
			elements = $("div.articles_output").children('h2[class="model_header"], div#timestamp, h3#userInputs');
	        elements = elements.add('table#inputsTable'); // user inputs
	        elements = elements.add('h4#pka, dl#pkaValues'); // pKa values
	        var parentTitle = $('table#msMain td:first h4');
	        var parentImage = $('#parent_div img'); // parent species
	        var parentTable = $('#parent_div table');
	        elements = elements.add(parentTitle).add(parentImage).add(parentTable);
	        var ms = $('table#msMain td#ms-cell').children().not($('div.chemspec_molecule'));
	        elements = elements.add(ms);
	        var majorMS = $('h4#majorMS, #majorMS_div img, #majorMS_div table');
	        elements = elements.add(majorMS);
	        var taut = $('h4#taut, p.taut-percent, #taut_div img, #taut_div table');
	        elements = elements.add(taut);
	        var stereo = $('h4#stereo, #stereo_div img, #stereo_div table');
	        elements = elements.add(stereo);
	        return elements;
	    case "pchemprop":
	    	elements = $('div.articles_output').children().not(':hidden, div#export_menu');
	    	return elements;
	   	case "gentrans":
	   		elements = $("div.articles_output").children('h2[class="model_header"], div#timestamp, h3#userInputs');
	        elements = elements.add('table#inputsTable'); // user inputs
	        elements = elements.add('h3#reactionPathways');
	        return elements;
	    default:
	    	elements = null;
	    	return elements;
	}
}


function buildCSV(workflow) {
	// build csv on backend, probably best considering batching
	var headers_array = [];
	var data_array = [];
	var content = []; // array with headers_array and data
	var prop_data = {
		"melting_point": [],
		"boiling_point": [],
		"water_sol": [],
		"vapor_press": [],
		"mol_diss": [],
		"ion_con": [],
		"henrys_law_con": [],
		"kow_no_ph": [],
		"kow_wph": [],
		"koc": []
	}; // {prop: [data, data, data, data]} in order of calc

	if (model == "pchemprop") {
		headers_array.push(""); // for formatting (keep rows same length)
		for (var calc in checkedCalcsAndProps) {
			if (checkedCalcsAndProps.hasOwnProperty(calc)) {
				for (var i = 0; i < calc.length; i++) {
					// looping props of calc..
					var calc_prop = checkedCalcsAndProps[calc][i];
					var data = $('.' + calc + '.' + calc_prop).html(); // get data from corresponding cell
					if (calc_prop == "ion_con") {
						data = pickOutPka(data);
					}
					if (data != null) {
						prop_data[calc_prop].push(data);
					}
				}
				headers_array.push(calc); // calcs
			}
		}
		content.push(headers_array);
		content.push(prop_data);
		// append calculator-independent data:
		content.push({
			"title": $('h2.model_header').html(),
			"time": time,
			"smiles": smiles,
			"name": name,
			"mass": mass,
			"formula": formula
		});
	}
	
	return content
}


function getWorkflow() {
	var path = window.location.href;
	if (path.indexOf("chemspec") > -1) {
		return "chemspec"
	}
	else if (path.indexOf("pchemprop") > -1) {
		return "pchemprop"
	}
	else if (path.indexOf("gentrans") > -1) {
		return "gentrans"		
	}
	else { return null; }
}


function pickOutPka(html_string) {
	var pkas = $.parseHTML(html_string);
	var pka_string = "";
	$(pkas).each(function () {
		var pka_html = $(this).text();
		pka_string += pka_html + " ";
	});
	return pka_string;
}