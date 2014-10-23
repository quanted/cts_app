$(window).load(function() {

  //read hidden textbox value for json string
  var jsonString = $('#jsonResult').val();
  jsonString = jsonString.replace('&quot;', '"');

  var metabProducts = JSON.parse(jsonString);

  var status = metabProducts.status;
  var results = metabProducts.results;
  // var imgs = jQuery('#showImages').is(':checked');
  var imgs = true;

  var addListItem = function(params) {
    var smiles = params.smiles;
    var iupac = params.iupac;
    var parentSmiles = params.parentSmiles;
    var routes = params.routes;
    
    // three lists for nearly the same reason, we should consolidate
    // list for pysiochemical API and saving properties
    if (list == "") {
      list = smiles + ';' + iupac;
    } else {
      list = list + ';' + smiles + ';' + iupac;
    }
    
    // list for GUI elements
    GUI.chemicalList[iupac] = smiles;

    // list for saving metabolites
    chemicals[smiles] = {};
    chemicals[smiles].parent = parentSmiles;
    chemicals[smiles].routes = routes;
    chemicals[smiles].iupac = iupac;
  };

  var metabolites = {};
  var parentSmiles = "";
  
  var recurseNodes = function(obj, treeObj, parentSmiles) {
    for (smiles in obj.metabolites) {
      if (obj.metabolites.hasOwnProperty(smiles)) {
        var content = getContent(smiles, obj.metabolites[smiles], imgs);
        addListItem({smiles:smiles,
                     parentSmiles:parentSmiles,
                     iupac:content.iupac,
                     routes:obj.metabolites[smiles].routes});/*,
                     rate:obj.metabolites[smiles].rate});*/
        
        var newObj = {};
        newObj.Content = content.html;
        newObj.Nodes = new Array();
        treeObj.Nodes.push(newObj);
        
        recurseNodes(obj.metabolites[smiles], newObj, smiles);
      }
    }
  }
  
  if (status == "success") {
    // hopefully this is only one
    // it should always be the smiles of the parent compound
    for (smiles in results) { 
      if (results.hasOwnProperty(smiles)) {
        var content = getContent(smiles, results[smiles], imgs);
        addListItem({smiles:smiles,
                     parentSmiles:null,
                     iupac:content.iupac,
                     routes:null});
        metabolites = {Content: content.html};
        metabolites.Nodes = new Array();
        recurseNodes(results[smiles], metabolites, smiles);
      }
    }
    
    DrawTree({
      Container: document.getElementById("degrade"),
      RootNode: metabolites,
      Layout: "Horizontal"
    });
    
    GUI.fillChemListControls();
  }
});