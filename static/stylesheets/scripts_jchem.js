var marvinSketcherInstance;


//Url mapping for ubertool-cts web services:
var Urls = {

  getChemDeats : "/jchem-cts/ws/getChemDeats/",
  mrvToSmiles : "/jchem-cts/ws/mrvToSmiles/",
  getChemSpecData : "/jchem-cts/ws/getChemSpecData/",

};


$(document).ready(function handleDocumentReady (e) {

  var p = MarvinJSUtil.getEditor("#sketch");
  p.then(function (sketcherInstance) {
    marvinSketcherInstance = sketcherInstance;
    // initControl(); //binds action to initControl() function
  }, function (error) {
    alert("Cannot retrieve sketcher instance from iframe:"+error);
  });  

  // $('#chemEditLookup').find('input:text').val(''); //clear all input fields at document load

  // $('#id_chem_struct').val('');
  // $('#molecule').val('');
  // $('#IUPAC').val('');
  // $('#formula').val('');
  // $('#weight').val('');


  // $('#setSmilesButton').on('click', { dataObj: null }, importMol(null));
  $('#setSmilesButton').on('click', {smiles:null}, importMol);
  $('#getSmilesButton').on('click', importMolFromCanvas);

});




function importMol(dataObj) {

  var objType = $.type(dataObj); //string if called by canvas, object or null otherwise

  var molTxt, iupacTxt, formTxt, weightTxt;

  var chemical;

  if (objType === "string")
  {
    chemical = dataObj;
  }
  else
  {
    chemical = $('#id_chem_struct').val();
  }

  if (chemical == "")
  {
    alert("Error getting chemical name, please try again...");
    return;
  }

  //Create POST data for web call:
  var params = new Object();
  params.url = Urls.getChemDeats;
  params.type = "POST";
  params.contentType = "application/json";
  params.dataType = "json";
  params.data = { "chemical" : chemical };

  var results = ajaxCall(params); //Get chemical information

  var data;

  if (typeof results !== "undefined") {
    data = results.data[0];
  }

  populateResultsTbl(data);

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

    if (results == 'Fail') {
      alert("Error getting data from server...");
      return;
    }
    else {
      // importMol(results["structure"]); //send data object 
      populateResultsTbl(results.data[0]);
    }

  });
}


function populateResultsTbl(data) {

  $('#id_chem_struct').val(data["smiles"]); //Enter SMILES txtbox
  $('#molecule').val(data["smiles"]); //SMILES string txtbox - results table
  $('#IUPAC').val(data["iupac"]); //IUPAC txtbox - results table
  $('#formula').val(data["formula"]); //Formula txtbox - results table
  $('#weight').val(data["mass"]); //Mass txtbox - results table

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