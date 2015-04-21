var marvinSketcherInstance;
var jchemGatewayUrl = "/jchem-cts/ws/traffic-cop/";
var portalUrl = "/cts/portal";


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

  var browserWidth = $(window).width();
  var browserHeight = $(window).height();
  var winleft = (browserWidth / 2) - 220 + "px";
  var wintop = (browserHeight / 2) - 30 + "px";

  //Removes error styling when focused on textarea or input:
  $('textarea, input').focusin(function() {
      if ($(this).hasClass('formError')) {
        $(this).removeClass("formError").val("");
      }
  });

  //redraw last chemcial if hitting back button from output:
  var chemical = $("#id_chem_struct").val();
  if (chemical != '' && chemical.indexOf('error') == -1) {
    importMol(chemical); 
  }

});


//"wait" cursor during ajax events
$(document).ajaxStart(function () {
    $('body').addClass('wait');
}).ajaxComplete(function () {
    $('body').removeClass('wait');
});


function importMol(dataObj) {
  //Gets formula, iupac, smiles, mass, and marvin structure 
  //for chemical in Lookup Chemical textarea

  var chemical = $('#id_chem_struct').val().trim();

  if (chemical == "") {
    displayErrorInTextbox("Enter a chemical or draw one first");
    return;
  }

  // ajaxCall(getParamsObj("getChemDetails", chemical), function(chemResults) {
  getChemDetails(chemical, function(chemResults) {
    if (chemResults != "Fail") {
      data = chemResults.data[0];
      populateResultsTbl(data);
      marvinSketcherInstance.importStructure("mrv", data.structureData.structure); //Load chemical to marvin sketch
    }
    else {
      displayErrorInTextbox("An error has occured during the call..sorry about that");
    }
  });

}


function importMolFromCanvas() {
  //Gets smiles, iupac, formula, mass for chemical 
  //drawn in MarvinJS

  marvinSketcherInstance.exportStructure("mrv").then(function(mrvChemical) {

    if (mrvChemical == '<cml><MDocument></MDocument></cml>') {
      displayErrorInTextbox("Draw a chemical, then try again");
      return;
    }

    mrvToSmiles(mrvChemical, function(smilesResult) {

      var smiles = smilesResult['structure'];

      getChemDetails(smiles, function(chemResults) {

        data = chemResults.data[0];
        populateResultsTbl(data);

      });

    });

    // ajaxCall(getParamsObj("mrvToSmiles", mrvChemical), function(smilesResult) {

    //   var smiles = smilesResult['structure'];
    //   ajaxCall(getParamsObj("getChemDetails", smiles), function(chemResults) {

    //       data = chemResults.data[0];
    //       populateResultsTbl(data);

    //   });

    // });

  });
}


function getChemDetails(chemical, callback) {
  ajaxCall(getParamsObj("getChemDetails", chemical), function(chemResults) {
    callback(chemResults);
  });
}


function mrvToSmiles(chemical, callback) {
  ajaxCall(getParamsObj("mrvToSmiles", chemical), function(smilesResult) {
    callback(smilesResult);
  });
}


function getParamsObj(service, chemical) {
  var params = new Object();
  params.url = portalUrl;
  params.type = "POST";
  // params.contentType = "application/json";
  params.dataType = "json";
  params.data = {"ws": "jchem", "service": service, "chemical": chemical}; // for portal
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
    errorMessage = "error retrieving chemical information...check chemical and try again.";
  }
  // $('#id_chem_struct').addClass("redFont");
  $('#id_chem_struct').addClass("formError");
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
      timeout: 10000,
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
      }

  });
}