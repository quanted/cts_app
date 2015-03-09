//testing polling events

var timer = null;

var updateTimer = function() {

  $.ajax({ 
    url: "/jchem-cts/ws/data",
    dataType: "json",
    success: function(data) {

      display_data(data);

    }
  });

  timer = setTimeout(updateTimer, 5000); // poll every 5s

};


function display_data(data) {
    // show the data acquired by load_data()

    //data is an array of Objects [0: {}, 1:{}, etc.]
    for (i in data) {

      var dataRow = data[i];

      if (dataRow.hasOwnProperty('running')) {
        //TODO: Change this, it's rewriting the same data
        $('.' + dataRow.calc + '.' + dataRow.prop).html(dataRow.val);
      }

      if (dataRow.running == false) {
        console.log("ending timeout (hopefully)");
        clearTimeout(timer);
      }

    }
}


$(document).ready(function() {
    updateTimer(); //initiate the timer
});