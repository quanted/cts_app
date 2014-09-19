var marvinSketcherInstance;


//Url mapping for ubertool-cts web services:
var Urls = {

  detailsBySmiles : "/services/detailsBySmiles/",
  mrvToSmiles : "/services/mrvToSmiles/",

}; //????


$(document).ready(function handleDocumentReady (e) {

  var p = MarvinJSUtil.getEditor("#sketch");
  p.then(function (sketcherInstance) {
    marvinSketcherInstance = sketcherInstance;
    // initControl(); //binds action to initControl() function
  }, function (error) {
    alert("Cannot retrieve sketcher instance from iframe:"+error);
  });  

  // $('#chemEditLookup').find('input:text').val(''); //clear all input fields at document load

  $('#id_chem_struct').val('');
  $('#molecule').val('');
  $('#IUPAC').val('');
  $('#formula').val('');
  $('#weight').val('');


  // $('#setSmilesButton').on('click', { dataObj: null }, importMol(null));
  $('#setSmilesButton').on('click', {smiles:null}, importMol);
  $('#getSmilesButton').on('click', importMolFromCanvas);

});




function importMol(dataObj) {

  var objType = $.type(dataObj); //string if called by canvas, object or null otherwise

  var molTxt, iupacTxt, formTxt, weightTxt;

  var chemical;

  if (objType === "string") {
    chemical = dataObj;
    // molTxt = dataObj["smiles"];
    // iupacTxt = dataObj["iupac"];
    // formTxt = dataObj["formula"];
    // weightTxt = dataObj["mass"];
  }
  else {

    chemical = $('#id_chem_struct').val();

    if (chemical == "") {
      return;
    }

    var params = new Object();
    params.url = Urls.detailsBySmiles;
    params.type = "POST";
    params.contentType = "application/json";
    params.dataType = "json";
    params.data = { "chemical" : chemical };

    var results = ajaxCall(params);

    var data = results.data[0];

    molTxt = data["smiles"];
    iupacTxt = data["iupac"];
    formTxt = data["formula"];
    weightTxt = data["mass"];

  } 

  // $('#molecule').val(data["smiles"]);
  // $('#IUPAC').val(data["iupac"]);
  // $('#formula').val(data["formula"]);
  // $('#weight').val(data["mass"]);

  $('#molecule').val(molTxt);
  $('#IUPAC').val(iupacTxt);
  $('#formula').val(formTxt);
  $('#weight').val(weightTxt);

  //Load chemical to marvin sketch:
  marvinSketcherInstance.importStructure("mrv", data.structureData.structure);

}


function importMolFromCanvas() {

  marvinSketcherInstance.exportStructure("mrv").then(function(source) {

    if (source == '<cml><MDocument></MDocument></cml>') {
      alert("Draw a chemical, then try again");
      return;
    }

    var params = new Object();
    // params.url = "test";
    params.url = Urls.mrvToSmiles;
    params.type = "POST";
    params.contentType = "application/json";
    params.dataType = "json";
    params.data = { "chemical" : source };

    var results = ajaxCall(params);

    // var smileData = REST.Util.MrvToSmiles(source);

    if (results == 'Fail') {
      alert("Error getting data from server...");
      return;
    }
    else {
      importMol(results["structure"]); //send data object 
    }

    // $.ajax({
    //   url : "/services/mrvToSmiles/",
    //   // url : "/REST/service/" + chemical,
    //   type : "POST",
    //   data : {
    //       "chemical" : source
    //     },
    //     //async: false,
    //   dataType : "json",
    //   success : function(response) {
    //     results = jsonRepack(response);


    //     var data = results.data[0];

    //   },
    //   error : function(jqXHR, textStatus, errorThrown) {
    //     results = "Fail ";
    //     console.log(" " + JSON.stringify(errorThrown));
    //   }
    // });

  });
}


function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}


function ajaxCall(params) {

  $.ajax({

      url : params.url,
      type : params.type,
      data : params.data,
      dataType : params.dataType,
      // contentType : params.contentType,

      success : function(response) {
        results = jsonRepack(response);
        // return results;
        // var data = results.data[0];
      },
      error : function(jqXHR, textStatus, errorThrown) {
        results = "Fail ";
        console.log(" " + JSON.stringify(errorThrown));
        // return results;
      },

  });

  return results;

}