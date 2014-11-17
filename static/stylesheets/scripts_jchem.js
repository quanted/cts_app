var marvinSketcherInstance;


//Url mapping for ubertool-cts web services:
var Urls = {

  getChemDeats : "/jchem-cts/ws/getChemDeats/",
  mrvToSmiles : "/jchem-cts/ws/mrvToSmiles/",
  getChemSpecData : "/jchem-cts/ws/getChemSpecData/",
  standarizer : "/jchem-cts/ws/standardizer/"

};


$(document).ready(function handleDocumentReady (e) {

  var p = MarvinJSUtil.getEditor("#sketch");
  p.then(function (sketcherInstance) {
    marvinSketcherInstance = sketcherInstance;
    // initControl(); //binds action to initControl() function
  }, function (error) {
    alert("Cannot retrieve sketcher instance from iframe:"+error);
  });  

  $('#setSmilesButton').on('click', importMol); // map button click to function
  $('#getSmilesButton').on('click', importMolFromCanvas);

  //Makes error message font red, then back to normal when focused
  $('#id_chem_struct')
    .focusin(function() {
      if ($(this).hasClass('redFont')) {
        $(this).removeClass("redFont").val("");
      }
  });

});


//Gets formula, iupac, smiles, mass, and marvin structure 
//for chemical in Lookup Chemical textarea
function importMol(dataObj) {

  var chemical = $('#id_chem_struct').val();

  if (chemical == "")
  {
    alert("Error getting chemical name, please try again...");
    return;
  }

  //Call standarizer first:
  var params = new Object();
  params.url = Urls.standarizer;
  params.type = "POST";
  params.contentType = "plain/text";
  params.dataType = "text";
  params.data = { "chemical" : chemical };
  var results = ajaxCall(params);

  if (typeof results === "undefined") {
    //TODO: send error message for populating table
    alert("Error retrieving chemical information...");
    return;
  }

  results = jQuery.parseJSON(results);

  if (results["status"] !== "success") {
    //TODO: send error message for populating table
    alert("Error retrieving chemical information...");
  }

  chemical = results["results"][0];

  //Create POST data for web call:
  params = new Object();
  params.url = Urls.getChemDeats;
  params.type = "POST";
  params.contentType = "application/json";
  params.dataType = "json";
  params.data = { "chemical" : chemical };

  results = ajaxCall(params); //Get chemical information

  if (typeof results !== "undefined") {
    data = results.data[0];
    populateResultsTbl(data);
    //Load chemical to marvin sketch:
    marvinSketcherInstance.importStructure("mrv", data.structureData.structure); 
  }
}


//Gets smiles, iupac, formula, mass for chemical 
//drawn in MarvinJS
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
      params = new Object();
      params.url = Urls.getChemDeats;
      params.type = "POST";
      params.contentType = "application/json";
      params.dataType = "json";
      params.data = {"chemical": results.structure};
      results = ajaxCall(params);
      populateResultsTbl(results.data[0]);
    }

  });
}


function populateResultsTbl(data) {

  var isError = false;

  $.each(data, function(key, value) {
    if (data[key].hasOwnProperty('error')) {
      isError = true;
    }
  });

  if (isError) {
    $('#id_chem_struct').addClass("redFont");
    $('#id_chem_struct').val("Error retrieving chemical information...Check chemical and try again."); //Enter SMILES txtbox
    $('#molecule').val(""); //SMILES string txtbox - results table
    $('#IUPAC').val(""); //IUPAC txtbox - results table
    $('#formula').val(""); //Formula txtbox - results table
    $('#weight').val(""); //Mass txtbox - results table
  }
  else {

    var type = typeof data["iupac"];

    $('#id_chem_struct').val(data["smiles"]); //Enter SMILES txtbox
    $('#molecule').val(data["smiles"]); //SMILES string txtbox - results table
    $('#IUPAC').val(data["iupac"]); //IUPAC txtbox - results table
    $('#formula').val(data["formula"]); //Formula txtbox - results table
    $('#weight').val(data["mass"]); //Mass txtbox - results table
  }
}


function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}


function ajaxCall(params) {

  var results = "";

  $.ajax({

      url : params.url,
      type : params.type,
      data : params.data,
      dataType : params.dataType,
      timeout: 1000,
      async: false,

      success : function(data, textStatus, callBack) {
        results = jsonRepack(data);
        // return results;
        // var data = results.data[0];
      },
      error : function(jqXHR, textStatus, errorThrown) {
        results = "Fail ";
        console.log(" " + JSON.stringify(errorThrown));
        alert("Error retrieving chemical information. Please try again.");
      },

  });

  return results;

}