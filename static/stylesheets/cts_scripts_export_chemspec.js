var doneDiv = document.getElementById("popup");

$(document).ready(function () {

	function parseOutput() {
		
		// var jq_html = $('<div />').append($("div.articles_output").children('H2[class="model_header"], table[class*=out_], div[class*=out_], H3[class*=out_], H4[class*=out_]:not(div#chart1,table:hidden)').clone()).html();

		// NOTE: This workflow wasn't having the default html capture due to its 
		// nested info, hidden plot data, etc. So for now it's pretty much hard coded (sorry)

		var elements = $("div.articles_output").children('h2[class="model_header"], div#timestamp, h3#userInputs');
		elements = elements.add('table#inputsTable'); // user inputs
		elements = elements.add('h4#pka, dl#pkaValues'); // pKa values
		
		var parentTitle = $('table#msMain td:first h4');
		var parentImage = $('#parent_div img'); // parent species
		var parentTable = $('#parent_div table');

		elements = elements
					.add(parentTitle)
					.add(parentImage)
					.add(parentTable); //.add(parentImage).add(parentTable);

		var ms = $('table#msMain td#ms-cell').children().not($('div.chemspec_molecule'));
		elements = elements.add(ms);

		var majorMS = $('h4#majorMS, #majorMS_div img, #majorMS_div table');
		elements = elements.add(majorMS);

		var jq_html = $('<div />').append($(elements).clone()).html();

		var n_plot_1 = $('div[id^="chart"]').size();
		var n_plot_2 = $('img[id^="chart"]').size();
		var n_plot = n_plot_1 + n_plot_2;

		console.log(n_plot);

		var i=1;

		var imgData = [];
		var options = {
			x_offset : 30,
			y_offset : 30
		};

		try { imgData.push($('#microspecies-distribution').jqplotToImageStr(options)); }
		catch(e) { console.log(e); }

		try { imgData.push($('#isoelectric-point').jqplotToImageStr(options)); }
		catch(e) { console.log(e); }


		var imgData_json = JSON.stringify(imgData, null, '\t');
		// console.log(imgData_json);
	
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

	}

	$('#pdfExport').click(function () {
		parseOutput();
		$('form').attr({'action': 'pdf', 'method': 'POST'}).submit();
		// $('form').attr('action', 'pdf').submit();
	});

	$('#htmlExport').click(function () {
		parseOutput();
		$('form').attr({'action': 'pdf', 'method': 'POST'}).submit();
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

});