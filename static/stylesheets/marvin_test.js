var marvinSketcherInstance;

$(document).ready(function handleDocumentReady (e) {

	// var p = MarvinJSUtil.getEditor("#sketch");
	// p.then(function (sketcherInstance) {
	// 	marvinSketcherInstance = sketcherInstance;
	// 	marvinSketcherInstance.importStructure("mol", s).catch(function(error) {
	// 		alert(error);
	// 	});
	// 	initControls();
	// }, function (error) {
	// 	alert("Cannot retrieve sketcher instance from iframe:"+error);
	// });

	//Create instance of Marvin sketch
	var p = MarvinJSUtil.getEditor("#sketch");
	p.then(function (sketcherInstance) {
		marvinSketcherInstance = sketcherInstance;
		initControl();
	}, function (error) {
		alert("Cannot retrieve sketcher instance from iframe:"+error);
	});


});

function initControls () {

	//Reset mol button (original code)
	// $("#getSmilesButton").on("click", function (e) {
	// 	marvinSketcherInstance.importStructure("mol", s);
	// });

	$("#getSmilesButton").on("click", function (e) {
		marvinSketcherInstance.exportStructure("mrv").then(function(source) {
			$("#molsource").text(source);
		}, function(error) {
			alert("Molecule export failed:"+error);	
		});
	});


}

var s = "\n\n\n"+
	" 14 15  0  0  0  0  0  0  0  0999 V2000\n"+
	"    0.5089    7.8316    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    1.2234    6.5941    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    1.2234    7.4191    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"   -0.2055    6.5941    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"   -0.9200    7.8316    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    0.5089    5.3566    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"   -0.2055    7.4191    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    0.5089    6.1816    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"   -0.9200    6.1816    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    0.5089    8.6566    0.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    2.4929    7.0066    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    2.0080    7.6740    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    2.0080    6.3391    0.0000 N   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"    2.2630    8.4586    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0\n"+
	"  1  7  1  0  0  0  0\n"+
	"  8  2  1  0  0  0  0\n"+
	"  1  3  1  0  0  0  0\n"+
	"  2  3  2  0  0  0  0\n"+
	"  7  4  1  0  0  0  0\n"+
	"  4  8  1  0  0  0  0\n"+
	"  4  9  2  0  0  0  0\n"+
	"  7  5  1  0  0  0  0\n"+
	"  8  6  1  0  0  0  0\n"+
	"  1 10  2  0  0  0  0\n"+
	"  3 12  1  0  0  0  0\n"+
	"  2 13  1  0  0  0  0\n"+
	" 13 11  2  0  0  0  0\n"+
	" 12 11  1  0  0  0  0\n"+
	" 12 14  1  0  0  0  0\n"+
	"M  END\n";

