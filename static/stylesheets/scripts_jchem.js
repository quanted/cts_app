var marvinSketcherInstance;
var portalUrl = "/cts/portal";

$(document).ready(function handleDocumentReady (e) {
  // var MarvinJSUtil;
  // if (MarvinJSUtil) {

  try {
    MarvinJSUtil.getEditor("#sketch").then(function (sketcherInstance) {
      marvinSketcherInstance = sketcherInstance;
      loadCachedChemical();
      // initControl(); //binds action to initControl() function
    }, function (error) {
      alert("Cannot retrieve sketcher instance from iframe:"+error);
    });
  }
  catch (e) {
    console.log("no marvin sketch instance here");
    return;
  }

  $('#setSmilesButton').on('click', importMol); // map button click to function
  $('#getSmilesButton').on('click', importMolFromCanvas);

  var browserWidth = $(window).width();
  var browserHeight = $(window).height();
  var winleft = (browserWidth / 2) - 220 + "px";
  var wintop = (browserHeight / 2) - 30 + "px";

  // Removes error styling when focused on textarea or input:
  $('textarea, input').focusin(function() {
      if ($(this).hasClass('formError')) {
        $(this).removeClass("formError").val("");
      }
  });

});


// "wait" cursor during ajax events
$(document).ajaxStart(function () {
    $('body').addClass('wait');
}).ajaxComplete(function () {
    $('body').removeClass('wait');
});


function loadCachedChemical() {
  var cached_molecule = JSON.parse(sessionStorage.getItem('molecule'));
  if (cached_molecule !== null) {
    populateChemEditDOM(cached_molecule);
  }
}


function importMol(chemical) {
  // Gets formula, iupac, smiles, mass, and marvin structure
  // for chemical in Lookup Chemical textarea

  if (typeof chemical !== 'string') {
    chemical = $('#id_chem_struct').val().trim();
  }

  if (chemical == "") {
    displayErrorInTextbox("Enter a chemical or draw one first");
    return;
  }

  var chemical_obj = {'chemical': chemical}; 
  
  getChemDetails(chemical_obj, function (molecule_info) {
    sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
    populateChemEditDOM(molecule_info.data);
    // marvinSketcherInstance.importStructure("mrv", molecule_info.data.structureData.structure);
  });

}


function importMolFromCanvas() {
  //Gets smiles, iupac, formula, mass for chemical 
  //drawn in MarvinJS
  marvinSketcherInstance.exportStructure("mrv").then(function(mrv_chemical) {
    if (mrv_chemical == '<cml><MDocument></MDocument></cml>') {
      displayErrorInTextbox("Draw a chemical first..");
      return;
    }

    var chemical_obj = {'chemical': mrv_chemical};

    getChemDetails(chemical_obj, function (molecule_info) {
      sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
      populateChemEditDOM(molecule_info.data);
      // marvinSketcherInstance.importStructure("mrv", molecule_info.data.structureData.structure);
    });
  });
}


function getChemDetails(chemical_obj, callback) {
  ajaxCall(chemical_obj, function (chemResults) {
    callback(chemResults);
  });
}


function populateChemEditDOM(data) {
  //Populates Results textboxes with data:
  $('#id_chem_struct').val(data["smiles"]); //Enter SMILES txtbox
  $('#molecule').val(data["smiles"]); //SMILES string txtbox - results table
  $('#orig-molecule').val(data['orig_smiles']);
  $('#IUPAC').val(data["iupac"]); //IUPAC txtbox - results table
  $('#formula').val(data["formula"]); //Formula txtbox - results table
  $('#weight').val(data["mass"]); //Mass txtbox - results table

  marvinSketcherInstance.importStructure("mrv", data.structureData.structure);

}


function displayErrorInTextbox(errorMessage) {
  //Displays error message in Lookup Chemical textbox
  if (typeof errorMessage === 'undefined' || errorMessage == "") {
    errorMessage = "error retrieving chemical information...please try again...";
  }
  $('#id_chem_struct').addClass("formError");
  $('#id_chem_struct').val(errorMessage); //Enter SMILES txtbox
  $('#molecule').val(""); //SMILES string txtbox - results table
  $('#IUPAC').val(""); //IUPAC txtbox - results table
  $('#formula').val(""); //Formula txtbox - results table
  $('#weight').val(""); //Mass txtbox - results table
  $('#orig-molecule').val("");
  try {
    marvinSketcherInstance.clear(); //clear marvin sketch
  }
  catch (e) {
    return;
  }
}


function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}


function ajaxCall(data_obj, callback) {
  $.ajax({
    url: '/cts/rest/molecule',
    type: 'POST',
    data: data_obj,
    dataType: 'json',
    timeout: 10000,
    success: function(data) {
      var data = jsonRepack(data);
      if (data.status == false) {
        displayErrorInTextbox(data.error);
      }
      else {
        $('#id_chem_struct').removeClass('formError');
        callback(data);
      }
    },
    error: function(jqXHR, textStatus, errorThrown) {
      displayErrorInTextbox("Error getting data for chemical");
    }
  });
}