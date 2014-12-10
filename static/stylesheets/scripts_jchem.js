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

  var browserWidth = $(window).width();
  var browserHeight = $(window).height();
  var winleft = (browserWidth / 2) - 220 + "px";
  var wintop = (browserHeight / 2) - 30 + "px";

});


//"wait" cursor during ajax events
$(document).ajaxStart(function ()
{
    $('body').addClass('wait');

}).ajaxComplete(function () {

    $('body').removeClass('wait');

});


//Gets formula, iupac, smiles, mass, and marvin structure 
//for chemical in Lookup Chemical textarea
function importMol(dataObj) {

  var chemical = $('#id_chem_struct').val();

  if (chemical == "") {
    displayErrorInTextbox("Enter a chemical or draw one first");
    return;
  }

  ajaxCall(standardizerObj(chemical), function(standardizerResult) {

      ajaxCall(mrvToSmilesObj(standardizerResult), function(smilesResult) {

          var smiles = smilesResult['structure'];
          ajaxCall(getChemDeatsObj(smiles), function(chemResults) {

              data = chemResults.data[0];
              populateResultsTbl(data);
              marvinSketcherInstance.importStructure("mrv", data.structureData.structure); //Load chemical to marvin sketch

          });

      });

  });

}


//Gets smiles, iupac, formula, mass for chemical 
//drawn in MarvinJS
function importMolFromCanvas() {

  marvinSketcherInstance.exportStructure("mrv").then(function(source) {

    if (source == '<cml><MDocument></MDocument></cml>') {
      displayErrorInTextbox("Draw a chemical, then try again");
      return;
    }

    ajaxCall(mrvToSmilesObj(source), function(smilesResult) {

      var smiles = smilesResult['structure'];
      ajaxCall(getChemDeatsObj(smiles), function(chemResults) {

          data = chemResults.data[0];
          populateResultsTbl(data);

      });

    });

  });
}


function standardizerObj(chemical) {
  //Forms request to call standardizer:
  var params = new Object();
  params.url = Urls.standarizer;
  params.type = "POST";
  params.contentType = "plain/text";
  params.dataType = "text";
  params.data = { "chemical" : chemical };
  return params;
}


function mrvToSmilesObj(chemical) {
  var params = new Object();
  params.url = Urls.mrvToSmiles;
  params.type = "POST";
  params.contentType = "application/json";
  params.dataType = "json";
  params.data = { "chemical" : chemical };
  return params;
}

function getChemDeatsObj(chemical) {
  var params = new Object();
  params.url = Urls.getChemDeats;
  params.type = "POST";
  params.contentType = "application/json";
  params.dataType = "json";
  params.data = { "chemical" : chemical };
  return params;
}


var error = false;
function containsErrors(results) {

  //Check results for a multitude of errors:
  if (typeof results === "undefined") {
    error = true;
  }
  else if (results == "Fail") {
    error = true;
  }
  else if (typeof results === "object") {
    $.each(results, dataWalker); //check n-nested object for errors
  }
  else if (typeof results === "string") {
    if (~results.indexOf("error")) {
      error = true;
    }
  }
  else {
    error = false;
  }

  if (error == true) {
    error = false;
    return true;
  }
  else {
    return false;
  }

}


function dataWalker(key, value) {
  // check key and value for error
  // var savePath = path;
  // path = path ? (path + "." + key) : key;

  if (typeof key === "string") {
    if (~key.indexOf("error")) {
      error = true;
      return false;
    }
  }
  else {
    if (key.hasOwnProperty("error")) {
      error = true;
      return false;
    }
  }

  if (typeof value === "string") {
    if (~value.indexOf("error")) {
      error = true;
      return false;
    }
  }
  else {
    if (value.hasOwnProperty("error")) {
      error = true;
      return false;
    }
  }

  if (value !== null && typeof value === "object") {
    $.each(value, dataWalker); //recurse into progeny
  }

}


function populateResultsTbl(data) {
  //Populates Results textboxes with data:
  $('#id_chem_struct').val(data["smiles"]); //Enter SMILES txtbox
  $('#molecule').val(data["smiles"]); //SMILES string txtbox - results table
  $('#IUPAC').val(data["iupac"]); //IUPAC txtbox - results table
  $('#formula').val(data["formula"]); //Formula txtbox - results table
  $('#weight').val(data["mass"]); //Mass txtbox - results table
}


function displayErrorInTextbox(errorMessage) {
  //Displays error message in Lookup Chemical textbox
  if (typeof errorMessage === 'undefined' || errorMessage == "") {
    errorMessage = "Error retrieving chemical information...Check chemical and try again.";
  }
  $('#id_chem_struct').addClass("redFont");
  $('#id_chem_struct').val(errorMessage); //Enter SMILES txtbox
  $('#molecule').val(""); //SMILES string txtbox - results table
  $('#IUPAC').val(""); //IUPAC txtbox - results table
  $('#formula').val(""); //Formula txtbox - results table
  $('#weight').val(""); //Mass txtbox - results table
  marvinSketcherInstance.clear(); //clear marvin sketch
}


function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}


function ajaxCall(params, callback) {
  $.ajax({
      url : params.url,
      type : params.type,
      data : params.data,
      dataType : params.dataType,
      success : function(data) {
        var data = jsonRepack(data);
        var isError = containsErrors(data);
        if (isError) {
          displayErrorInTextbox();
          return;
        }
        else {
          callback(jsonRepack(data));
        }
      },
      error : function(jqXHR, textStatus, errorThrown) {
        callback("Fail");
      },

  });
}