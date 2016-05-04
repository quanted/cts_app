var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);

var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');


// var express = require('express');
// var app = express();

// app.get('/test', function (req, res) {
//     res.send("i'm up and running!");
// });

// app.listen(4001, function () {
//     console.log("listening on 4001");
// });


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
    // io.set('resource', 'cts/socket');  // not sure about this one
});



io.sockets.on('connection', function (socket) {

    // var sessionid = socket.handshake.cookie['sessionid']; // use cookie set by django..

    var message_client = redis.createClient();

    console.log("node redis client established: " + message_client);
    message_client.subscribe(socket.id); // create channel with client's socket id
    
    // Grab message from Redis that was created by django and send to client
    message_client.on('message', function(channel, message){
        console.log("reading message from redis: " + message + " on channel: " + channel);
        socket.send(message); // send to browser
    });

    console.log("session id: " + socket.id);

    // for web socket testing:
    socket.on('say_hello', function (message) {
        console.log("node received message: ");
        console.log(message);
        socket.send("hello client " + socket.id);
    });

    socket.on('test_celery', function (message) {
        console.log("received message: " + message);
        var query = querystring.stringify({
            sessionid: socket.id, // cts will now publish to session channel
            message: message
        });

        passRequestToCTS(query);
    });
    
    // checked calcs/props sent from front-end:
    socket.on('get_data', function (message) {

        console.log("nodejs server received message..");

        var message_obj = JSON.parse(message);

        var values = {};
        for (var key in message_obj) {
            if (message_obj.hasOwnProperty(key)) {
                if (key == 'props') {
                    values[key + '[]'] = message_obj[key];
                }
                else {
                    values[key] = message_obj[key];
                }
            }
        }

        var query = querystring.stringify({
            sessionid: socket.id,
            message: JSON.stringify(values)
        });

        passRequestToCTS(query);

    });

    socket.on('disconnect', function () {
        console.log("user " + socket.id + " disconnected..");
        message_client.unsubscribe(socket.id); // unsubscribe from channel
        //console.log("user " + socket.id + " unsubscribed from redis channel..");

        var message_obj = {'cancel': true};

        var query = querystring.stringify({
            sessionid: socket.id,
            message: JSON.stringify(message_obj)
        });

        passRequestToCTS(query);

    });

});

function passRequestToCTS (values) {
    var options = {
        host: 'localhost',
        // port: 8000,
        // host: '134.67.114.1',
        port: 8081,
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