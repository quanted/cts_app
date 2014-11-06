function buildInfoTable(info) {
	var structInfo = {
						"Formula": info.formula, 
				 		"IUPAC": info.iupac,
				 	 	"SMILES": info.smiles,
				 	  	"Mass": info.mass
					};

	//popup table on mouseover event
	var htmlWrapper = "<table>"
 	for (var key in structInfo) {
 		if (structInfo.hasOwnProperty(key)) {
 			htmlWrapper += "<tr><td>";
 			htmlWrapper += key; 
 			htmlWrapper += "</td><td>";
 			htmlWrapper += structInfo[key];
 			htmlWrapper += "</td></tr>";
 		}
 	}
 	htmlWrapper += "</table>";

 	return htmlWrapper;
 }