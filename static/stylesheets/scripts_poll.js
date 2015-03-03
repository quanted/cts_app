//testing polling events

(function poll() {

   setTimeout(function() {

       $.ajax({ url: "/jchem-cts/ws/data", success: function(data) {
            // sales.setValue(data.value);
            console.log(data.value);
       }, dataType: "json", complete: poll });

    }, 20000);

})();


function display_data(data) {
    // show the data acquired by load_data()
    $('#poll-test').html(data.value);
}


$(document).ready(function() {
    // load the initial data (assuming it will be immediately available)
    // load_data();
});