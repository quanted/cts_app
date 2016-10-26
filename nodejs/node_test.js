// var express = require('express');
// var app = express();

// app.get('/', function(req, res){
//   res.send('hello world');
// });

// app.listen(3000);



// var http = require('http');
// var server = http.createServer().listen(4000);
// var io = require('socket.io').listen(server);

// io.sockets.on('connection', function (socket) {

//     console.log("session id: " + socket.id);

//     // for web socket testing:
//     socket.on('say_hello', function (message) {
//         console.log("node received message: ");
//         console.log(message);
//         socket.send("hello client " + socket.id);
//     });

//     socket.on('disconnect', function () {
//         console.log("user " + socket.id + " disconnected..");
//     });

// });



// var engine = require('engine.io');
// var server = engine.listen(4000);
// var http = require('http');
// var redis = require('redis');
// var querystring = require('querystring');
var http = require('http');
var server = http.createServer().listen(4000);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
var redis = require('redis');

console.log("nodejs + engine.io server at port 4000...");


// server.on('connection', function(socket){
io.on('connection', function (socket) {
    console.log("client " + socket.id + " connected...");
    // socket.send('utf 8 string');
    // socket.send(new Buffer([0, 1, 2, 3, 4, 5])); // binary data


    // console.log("socket connection made...");


    // var message_client = redis.createClient();

    // console.log("node redis client established: " + message_client);
    // message_client.subscribe(socket.id); // create channel with client's socket id
    
    // // Grab message from Redis that was created by django and send to client
    // message_client.on('message', function(channel, message){
    //     // console.log("reading message from redis: " + message + " on channel: " + channel);
    //     console.log("reading message from redis on channel: " + channel);
    //     socket.send(message); // send to browser
    // });

    // console.log("session id: " + socket.id);

    // for web socket testing:
    socket.on('say_hello', function (message) {
        console.log("node received message: ");
        console.log(message);
        // socket.send("hello client " + socket.id);
    });

    // socket.on('test_celery', function (message) {
    //     console.log("received message: " + message);
    //     var query = querystring.stringify({
    //         sessionid: socket.id, // cts will now publish to session channel
    //         message: message
    //     });
    //     passRequestToCTS(query);
    // });
    
    // // checked calcs/props sent from front-end:
    // socket.on('get_data', function (message) {
    //     console.log("nodejs server received message..");
    //     var message_obj = JSON.parse(message);
    //     var values = {};
    //     for (var key in message_obj) {
    //         if (message_obj.hasOwnProperty(key)) {
    //             if (key == 'props') {
    //                 values[key + '[]'] = message_obj[key];
    //             }
    //             else {
    //                 values[key] = message_obj[key];
    //             }
    //         }
    //     }
    //     var query = querystring.stringify({
    //         sessionid: socket.id,
    //         message: JSON.stringify(values)
    //     });
    //     passRequestToCTS(query);
    // });

    // socket.on('disconnect', function () {
    //     console.log("user " + socket.id + " disconnected..");
    //     message_client.unsubscribe(socket.id); // unsubscribe from channel
    //     //console.log("user " + socket.id + " unsubscribed from redis channel..");
    //     var message_obj = {'cancel': true};
    //     var query = querystring.stringify({
    //         sessionid: socket.id,
    //         message: JSON.stringify(message_obj)
    //     });
    //     passRequestToCTS(query);
    // });

});

function passRequestToCTS (values) {
    var options = {
        host: 'localhost',
        // port: 8081,  // this along with localhost is for cgi server 1
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