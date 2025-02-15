var ketcherFrame = null;

$(document).ready(function handleDocumentReady (e) {});

function initiateKetcherInstance(jchem_server) {

  try {
    ketcherFrame = document.getElementById('ifKetcher');
    loadCachedChemical();
  }
  catch (e) {
    console.log("Error getting ketcher instance: ", e)
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
}

function getKetcherInstance() {
  return ketcherFrame.contentWindow.ketcher;
}

// "wait" cursor during ajax events
$(document).ajaxStart(function () {
    $('body').addClass('wait');
}).ajaxComplete(function () {
    $('body').removeClass('wait');
});

function loadCachedChemical() {
  var cachedMolecule = JSON.parse(sessionStorage.getItem('molecule'));
  if (cachedMolecule !== null) {

    setTimeout(() => {
      populateChemEditDOM(cachedMolecule);
      // Checking for missing MarvinSketch, if there isn't
      // <cml> data for it, then it requests it:
      checkForKetcherData(cachedMolecule);
    }, 1000);

  }
}

function checkForKetcherData(cachedMolecule) {
  // Checks for missing MarvinSketch, if there isn't
  // <cml> data for it, then it requests it:
  if (!('structureData' in cachedMolecule)) {
    var chemicalObj = {'chemical': cachedMolecule.chemical, 'get_structure_data': true};
    getChemDetails(chemicalObj, function (molecule_info) {
      sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
      populateChemEditDOM(molecule_info.data);
    });
  }
}

function importMol(chemical) {
  // Gets formula, iupac, smiles, mass, and marvin structure
  // for chemical in Lookup Chemical textarea

  clearChemicalEditorContent(true);  // clears ketcher and results table

  if (typeof chemical !== 'string') {
    chemical = $('#id_chem_struct').val().trim();
  }
  if (chemical == "") {
    displayErrorInTextbox("Enter a chemical or draw one first");
    return;
  }
  var chemical_obj = {'chemical': chemical, 'get_structure_data': true};  // script for chmical editor tab needs structureData <cml> image for marvin sketch 
  getChemDetails(chemical_obj, function (molecule_info) {
    sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
    populateChemEditDOM(molecule_info.data);
  });
  
}

function importMolFromCanvas() {
  /*
  Gets smiles, iupac, formula, mass for chemical 
  drawn in MarvinJS.
  */
  clearChemicalEditorContent(false);  // clears ketcher and results table
  $('#id_chem_struct').val(""); // clears 'Lookup Chemical' before loading new one from drawn molecule

  // getKetcherInstance().getSmilesAsync().then((smilesFromStructre) => {
  getKetcherInstance().getSmiles().then((smilesFromStructre) => {

    if (smilesFromStructre.length < 1) {
      displayErrorInTextbox("Draw a chemical first..");
      return;
    }

    var chemical_obj = {'chemical': smilesFromStructre, 'get_structure_data': true};
    getChemDetails(chemical_obj, function (molecule_info) {
      // put orig smiles in "lookup chemical" box for drawn chemical:
      molecule_info['data']['chemical'] = molecule_info['data']['orig_smiles'];
      sessionStorage.setItem('molecule', JSON.stringify(molecule_info.data)); // set current chemical in session cache
      populateChemEditDOM(molecule_info.data);
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
  $('#id_chem_struct').val(data["chemical"]); //Enter SMILES txtbox
  $('#chemical').val(data['chemical']);
  $('#smiles').val(data["smiles"]); //SMILES string txtbox - results table
  $('#orig_smiles').val(data['orig_smiles']);
  $('#preferredName').val(data['preferredName']);
  $('#iupac').val(data["iupac"]); //IUPAC txtbox - results table
  $('#formula').val(data["formula"]); //Formula txtbox - results table
  $('#cas').val(data['cas']);
  $('#casrn').val(data['casrn']);
  $('#dtxsid').val(data['dtxsid']);
  $('#mass').val(data["mass"]); //Mass txtbox - results table
  $('#exactmass').val(data['exactMass']);
  try {
    getKetcherInstance().setMolecule(data.structureData.structure);
  }
  catch (e) {
    console.error(e);
  }
}

function displayErrorInTextbox(errorMessage) {
  //Displays error message in Lookup Chemical textbox
  if (typeof errorMessage === 'undefined' || errorMessage == "") {
    errorMessage = "Name not recognized..";
  }
  $('#id_chem_struct').addClass("formError").val(errorMessage); //Enter SMILES txtbox
  clearChemicalEditorContent(true);
}

function clearChemicalEditorContent(clearDrawer) {
  // Clears MarvinSketch instance and results table
  $('#chemical').val("");
  $('#smiles').val("");
  $('#orig_smiles').val("");
  $('#preferredName').val("");
  $('#iupac').val("");
  $('#formula').val("");
  $('#cas').val("");
  $('#casrn').val("");
  $('#dtxsid').val("");
  $('#mass').val("");
  $('#exactmass').val("");
  if (clearDrawer === true) {
    getKetcherInstance().editor.struct(null); // https://github.com/epam/ketcher/issues/26
  }
}

function jsonRepack(jsonobj) {
  return JSON.parse(JSON.stringify(jsonobj));
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}     

var csrftoken = getCookie('csrftoken');

function ajaxCall(data_obj, callback) {
  $.ajax({
    url: '/cts/rest/molecule',
    type: 'POST',
    data: data_obj,
    dataType: 'json',
    // timeout: 10000,
    timeout: 30000,
    tryCount: 0,
    retryLimit: 1,  // retry 1 time if failure
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
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
      if (textStatus == 'timeout' || textStatus == 'error') {
        this.tryCount++;
        if (this.tryCount <= this.retryLimit) {
          // try again
          $.ajax(this);
          return;
        }
        displayErrorInTextbox("Name not recognized");
        return;
      }
      else {
        displayErrorInTextbox("Name not recognized");
        return;
      }
    }
  });

}