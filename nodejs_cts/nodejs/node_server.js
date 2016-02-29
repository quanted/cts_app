var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');

// client = redis.createClient();
// console.log("node redis client established: " + client);

//Configure socket.io to store cookie set by Django
io.configure(function(){
    io.set('authorization', function(data, accept){
        if(data.headers.cookie){
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        return accept('error', false);
    });
    io.set('log level', 1);
});

io.sockets.on('connection', function (socket) {

    // var sessionid = socket.handshake.cookie['sessionid']; // use cookie set by django..


    // send socket id to cts backend upon client connection:
    var values = querystring.stringify({
        message: "start new session",
        sessionid: socket.id,
        ws: "new_session"
    });
    callCTSNodeAPI(values);


    var client = redis.createClient();
    console.log("node redis client established: " + client);
    client.subscribe(socket.id); // create channel with client's socket id
    
    // Grab message from Redis that was created by django and send to client
    client.on('message', function(channel, message){
        console.log("reading message from redis: " + message + " on channel: " + channel);
        socket.send(message); // send to browser
    });

    console.log("session id: " + socket.id);
    
    // checked calcs/props sent from front-end:
    socket.on('get_data', function (message) {

        console.log("nodejs server received message..");

        // should calls be parsed out here, or after cts portal???
        // i'm going to try it from django first (node_api views)

        var web_service = message.ws; // node_api
        //var all_data = message['data'];

        //for (calc in all_data) {
        //
        //    var calc_data = all_data[calc]; // prop data array
        //    var post_data = {'chemical': message['chem'], 'calc': calc};
        //
        //    if (calc == "test") {
        //        for (var i = 0; i < calc_data.length; i++) {
        //            post_data['prop'] = calc_data[i];
        //            var values = querystring.stringify({
        //                message: post_data,
        //                sessionid: socket.id,
        //                ws: web_service
        //            });
        //            callCTSNodeAPI(values); // send off to cts backend, node_api views!
        //        }
        //    }
        //}

        message = JSON.stringify(message);

        console.log("message: ");
        console.log(message);

        values = querystring.stringify({
            message: message, // this key is the event name for client.on() above..
            sessionid: socket.id,
            ws: web_service
        });

        console.log("values established");
        console.log(values);

        callCTSNodeAPI(values);

    });

    socket.on('disconnect', function () {
        console.log("client " + socket.id + " disconnected..");
        client.unsubscribe(socket.id); // unsubscribe from channel
        console.log("client unsubscribed from redis channel..");
    });

});

function callCTSNodeAPI (values) {

    var options = {
        host: 'localhost',
        port: 8000,
        path: '/cts/portal',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': values.length
        }
    };

    // Send message to CTS server:
    var req = http.request(options, function(res){
        res.setEncoding('utf8');        
        // Print out error message:
        res.on('data', function(message){
            if(message != 'Everything worked :)'){
                console.log('Message: ' + message);
            } 
        });
    });
    req.write(values);
    req.end();

}